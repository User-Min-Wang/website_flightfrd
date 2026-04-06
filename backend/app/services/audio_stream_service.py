import threading
import websocket
import json
import logging
import io
import tempfile
from datetime import datetime
from typing import Optional, Dict, List
from extensions import db, socketio
from app.models import ATCMessage
from app.services.atc_service import ATCService

logger = logging.getLogger(__name__)


class AudioStreamService:
    """
    管理 ATC 音频流连接和处理
    
    功能：
    - 连接音频源（LiveATC.net 或 SDR）
    - 实时语音转文字（使用 Whisper）
    - 消息分类和呼号提取
    - 通过 WebSocket 推送实时消息
    - 支持多频道管理
    """
    
    def __init__(self):
        self.active_streams: Dict[str, threading.Thread] = {}
        self.stream_configs: Dict[str, dict] = {}
        self.atc_service = ATCService()
        self.whisper_model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """加载 Whisper 语音识别模型"""
        try:
            import whisper
            self.whisper_model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except ImportError:
            logger.warning("Whisper not installed. Speech-to-text will be unavailable.")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
    
    def start_stream(self, stream_id: str, stream_url: str, frequency: str, 
                     airport_code: str, channel_name: str = "default"):
        """
        启动音频流监听
        
        Args:
            stream_id: 流的唯一标识符
            stream_url: 音频流 URL (WebSocket 或 HTTP)
            frequency: 频率 (e.g., "118.700")
            airport_code: 机场代码 (e.g., "KJFK")
            channel_name: 频道名称 (e.g., "Tower", "Ground", "Approach")
        """
        if stream_id in self.active_streams:
            logger.warning(f"Stream {stream_id} already active")
            return False
        
        # 保存流配置
        self.stream_configs[stream_id] = {
            'stream_url': stream_url,
            'frequency': frequency,
            'airport_code': airport_code,
            'channel_name': channel_name,
            'started_at': datetime.utcnow()
        }
        
        # 创建并启动处理线程
        thread = threading.Thread(
            target=self._listen_to_stream,
            args=(stream_id,),
            daemon=True
        )
        thread.start()
        self.active_streams[stream_id] = thread
        
        logger.info(f"Started stream {stream_id} for frequency {frequency} ({channel_name})")
        
        # 发送流启动事件
        socketio.emit('stream_started', {
            'stream_id': stream_id,
            'frequency': frequency,
            'channel_name': channel_name,
            'airport_code': airport_code
        }, namespace='/atc')
        
        return True
    
    def stop_stream(self, stream_id: str):
        """停止音频流"""
        if stream_id not in self.active_streams:
            logger.warning(f"Stream {stream_id} not found")
            return False
        
        # 标记流为停止状态（线程会自行退出）
        if stream_id in self.stream_configs:
            self.stream_configs[stream_id]['stopped'] = True
        
        # 从活动列表中移除
        del self.active_streams[stream_id]
        
        logger.info(f"Stopped stream {stream_id}")
        
        # 发送流停止事件
        socketio.emit('stream_stopped', {
            'stream_id': stream_id
        }, namespace='/atc')
        
        return True
    
    def get_active_streams(self) -> List[dict]:
        """获取所有活动流的信息"""
        streams = []
        for stream_id, config in self.stream_configs.items():
            streams.append({
                'stream_id': stream_id,
                'frequency': config.get('frequency'),
                'airport_code': config.get('airport_code'),
                'channel_name': config.get('channel_name'),
                'started_at': config.get('started_at').isoformat() if config.get('started_at') else None,
                'is_active': stream_id in self.active_streams
            })
        return streams
    
    def _listen_to_stream(self, stream_id: str):
        """
        监听音频流并处理
        
        这是一个长期运行的线程，会持续接收音频数据并进行处理
        """
        config = self.stream_configs.get(stream_id)
        if not config:
            logger.error(f"Configuration not found for stream {stream_id}")
            return
        
        stream_url = config['stream_url']
        frequency = config['frequency']
        airport_code = config['airport_code']
        channel_name = config['channel_name']
        
        try:
            # 根据 URL 类型选择连接方式
            if stream_url.startswith('ws://') or stream_url.startswith('wss://'):
                self._handle_websocket_stream(stream_id, stream_url, frequency, airport_code, channel_name)
            else:
                self._handle_http_stream(stream_id, stream_url, frequency, airport_code, channel_name)
                
        except Exception as e:
            logger.error(f"Stream error for {stream_id}: {str(e)}")
            socketio.emit('stream_error', {
                'stream_id': stream_id,
                'error': str(e)
            }, namespace='/atc')
        finally:
            # 清理
            if stream_id in self.active_streams:
                del self.active_streams[stream_id]
    
    def _handle_websocket_stream(self, stream_id: str, stream_url: str, 
                                  frequency: str, airport_code: str, channel_name: str):
        """处理 WebSocket 音频流"""
        ws = websocket.create_connection(stream_url, timeout=30)
        logger.info(f"Connected to WebSocket stream: {stream_url}")
        
        audio_buffer = bytearray()
        
        while stream_id in self.active_streams and not self.stream_configs.get(stream_id, {}).get('stopped'):
            try:
                # 接收音频数据
                audio_data = ws.recv()
                
                if isinstance(audio_data, bytes):
                    audio_buffer.extend(audio_data)
                    
                    # 每积累一定大小的音频数据就进行处理
                    if len(audio_buffer) >= 64000:  # 约 2 秒的音频
                        self._process_audio_buffer(
                            stream_id, 
                            bytes(audio_buffer), 
                            frequency, 
                            airport_code, 
                            channel_name
                        )
                        audio_buffer = bytearray()
                        
            except websocket.WebSocketConnectionClosedException:
                logger.warning(f"WebSocket connection closed for stream {stream_id}")
                break
            except Exception as e:
                logger.error(f"Error receiving data from stream {stream_id}: {str(e)}")
                break
        
        ws.close()
    
    def _handle_http_stream(self, stream_id: str, stream_url: str,
                            frequency: str, airport_code: str, channel_name: str):
        """处理 HTTP 音频流（如 Icecast/Shoutcast）"""
        import requests
        
        session = requests.Session()
        
        try:
            response = session.get(stream_url, stream=True, timeout=30)
            response.raise_for_status()
            
            logger.info(f"Connected to HTTP stream: {stream_url}")
            
            audio_buffer = bytearray()
            
            for chunk in response.iter_content(chunk_size=8192):
                if stream_id not in self.active_streams or self.stream_configs.get(stream_id, {}).get('stopped'):
                    break
                
                if chunk:
                    audio_buffer.extend(chunk)
                    
                    # 每积累一定大小的音频数据就进行处理
                    if len(audio_buffer) >= 64000:
                        self._process_audio_buffer(
                            stream_id,
                            bytes(audio_buffer),
                            frequency,
                            airport_code,
                            channel_name
                        )
                        audio_buffer = bytearray()
                        
        except Exception as e:
            logger.error(f"HTTP stream error for {stream_id}: {str(e)}")
        finally:
            session.close()
    
    def _process_audio_buffer(self, stream_id: str, audio_data: bytes,
                              frequency: str, airport_code: str, channel_name: str):
        """
        处理音频缓冲区：语音转文字、分类、存储和推送
        
        Args:
            stream_id: 流 ID
            audio_data: 原始音频数据
            frequency: 频率
            airport_code: 机场代码
            channel_name: 频道名称
        """
        if not self.whisper_model:
            return
        
        try:
            # 将音频数据保存为临时文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                f.write(audio_data)
                temp_path = f.name
            
            # 使用 Whisper 进行语音转文字
            result = self.whisper_model.transcribe(temp_path, language='en')
            text = result['text'].strip()
            confidence = result.get('language_probability', 0.0)
            
            if text:
                logger.info(f"Transcribed: {text}")
                
                # 提取呼号
                callsign = self._extract_callsign(text)
                
                # 分类消息
                message_type = self._classify_message(text)
                
                # 判断是否为紧急通信
                is_emergency = self._is_emergency(text)
                
                # 确定优先级
                priority_level = self._calculate_priority(message_type, is_emergency)
                
                # 存储到数据库
                atc_message = self.atc_service.store_atc_message(
                    frequency=frequency,
                    callsign=callsign,
                    message_content=text,
                    message_type=message_type,
                    sender_type=self._identify_sender(text, callsign),
                    airport_code=airport_code,
                    channel=channel_name,
                    is_emergency=is_emergency,
                    priority_level=priority_level,
                    transcription_confidence=confidence
                )
                
                # 通过 WebSocket 推送给前端
                message_data = atc_message.to_dict()
                message_data['channel_name'] = channel_name
                
                # 推送到特定频道房间
                socketio.emit('new_atc_message', message_data, 
                             room=f"{airport_code}_{channel_name}", 
                             namespace='/atc')
                
                # 也推送到所有订阅该频率的客户端
                socketio.emit('new_atc_message', message_data, 
                             room=frequency, 
                             namespace='/atc')
                
                # 如果有翻译服务，添加翻译
                translated_text = self._translate_message(text)
                if translated_text and translated_text != text:
                    message_data['translated_content'] = translated_text
                    socketio.emit('message_translated', message_data,
                                 room=f"{airport_code}_{channel_name}",
                                 namespace='/atc')
            
            import os
            os.unlink(temp_path)
            
        except Exception as e:
            logger.error(f"Error processing audio buffer: {str(e)}")
    
    def _extract_callsign(self, text: str) -> Optional[str]:
        """从文本中提取航空呼号"""
        import re
        
        # 常见的航空呼号模式
        patterns = [
            r'\b([A-Z]{2,3}\d+[A-Z]?)\b',  # 如 AAL123, UAL456B
            r'\b([A-Z]{3}\s*\d+[A-Z]?)\b',  # 如 AAL 123
            r'\b(N\d+[A-Z]{1,3})\b',  # 美国通用航空 N 注册号
            r'\b(CES\d+)\b',  # 如 CES5401
        ]
        
        text_upper = text.upper()
        for pattern in patterns:
            match = re.search(pattern, text_upper)
            if match:
                return match.group(1).replace(' ', '')
        
        return None
    
    def _classify_message(self, text: str) -> str:
        """
        分类 ATC 消息类型
        
        Returns:
            str: 消息类型 (clearance, contact, taxi, takeoff, landing, position, emergency, other)
        """
        text_lower = text.lower()
        
        # 紧急通信
        if any(word in text_lower for word in ['mayday', 'pan pan', 'emergency', 'declaring emergency']):
            return 'emergency'
        
        # 起飞许可
        if any(phrase in text_lower for phrase in ['cleared for takeoff', 'takeoff cleared', 'line up and wait']):
            return 'takeoff'
        
        # 降落许可
        if any(phrase in text_lower for phrase in ['cleared to land', 'cleared for landing', 'cleared approach']):
            return 'landing'
        
        # 滑行指令
        if any(word in text_lower for word in ['taxi', 'pushback', 'push back']):
            return 'taxi'
        
        # 放行许可
        if any(phrase in text_lower for phrase in ['cleared to', 'flight plan', 'departure clearance']):
            return 'clearance'
        
        # 联系指令
        if 'contact' in text_lower or 'monitor' in text_lower:
            return 'contact'
        
        # 位置报告
        if any(word in text_lower for word in ['position', 'reporting', 'passing', 'descending', 'climbing']):
            return 'position'
        
        return 'other'
    
    def _is_emergency(self, text: str) -> bool:
        """判断是否为紧急通信"""
        text_lower = text.lower()
        return any(word in text_lower for word in ['mayday', 'pan pan', 'emergency', 'fuel emergency'])
    
    def _calculate_priority(self, message_type: str, is_emergency: bool) -> int:
        """
        计算消息优先级 (1-5, 5 为最高)
        
        Returns:
            int: 优先级级别
        """
        if is_emergency:
            return 5
        
        priority_map = {
            'emergency': 5,
            'takeoff': 4,
            'landing': 4,
            'contact': 3,
            'clearance': 3,
            'taxi': 2,
            'position': 2,
            'other': 1
        }
        
        return priority_map.get(message_type, 1)
    
    def _identify_sender(self, text: str, callsign: Optional[str]) -> str:
        """
        识别发送者类型
        
        Returns:
            str: sender_type (pilot, controller, station)
        """
        # 简化的逻辑：如果有呼号，通常是飞行员；否则可能是管制员
        if callsign:
            return 'pilot'
        
        text_lower = text.lower()
        if any(word in text_lower for word in ['contact', 'cleared', 'turn left', 'turn right', 'maintain']):
            return 'controller'
        
        return 'station'
    
    def _translate_message(self, text: str, target_language: str = 'zh') -> Optional[str]:
        """
        翻译 ATC 消息（可选功能）
        
        Args:
            text: 原文本
            target_language: 目标语言 (默认中文)
            
        Returns:
            str: 翻译后的文本，如果翻译失败则返回 None
        """
        # 这里可以集成翻译 API（如 Google Translate, DeepL 等）
        # 示例代码：
        try:
            # from googletrans import Translator
            # translator = Translator()
            # result = translator.translate(text, dest=target_language)
            # return result.text
            
            # 临时返回原文（实际使用时需要实现真正的翻译）
            return None
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return None


# 全局实例
audio_stream_service = AudioStreamService()
