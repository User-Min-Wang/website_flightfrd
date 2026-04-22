#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenSky Network API 使用示例
============================
提供实时航班查询、特定飞机追踪、历史轨迹查询等功能

使用前请注册免费账号：https://opensky-network.org/register
"""

import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class OpenSkyAPI:
    """OpenSky Network API 封装类"""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        初始化 API 客户端
        
        Args:
            username: OpenSky 用户名（可选，建议注册后使用）
            password: OpenSky 密码（可选）
        """
        self.base_url = "https://opensky-network.org/api"
        self.username = username
        self.password = password
        self.session = requests.Session()
        
        if username and password:
            self.session.auth = (username, password)
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """发送 API 请求"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("❌ 认证失败，请检查用户名和密码")
            elif e.response.status_code == 429:
                print("⚠️  请求过于频繁，已达到速率限制")
            else:
                print(f"❌ HTTP 错误：{e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求错误：{e}")
            return None
    
    def get_all_states(self, 
                       latitude_min: Optional[float] = None,
                       longitude_min: Optional[float] = None,
                       latitude_max: Optional[float] = None,
                       longitude_max: Optional[float] = None) -> Optional[List[Dict]]:
        """
        获取所有航班实时状态
        
        Args:
            latitude_min: 最小纬度
            longitude_min: 最小经度
            latitude_max: 最大纬度
            longitude_max: 最大经度
            
        Returns:
            航班状态列表
        """
        params = {}
        if all([latitude_min, longitude_min, latitude_max, longitude_max]):
            params['lamin'] = latitude_min
            params['lomin'] = longitude_min
            params['lamax'] = latitude_max
            params['lomax'] = longitude_max
        
        data = self._make_request("states/all", params)
        if not data or 'states' not in data:
            return None
        
        # 将数组转换为字典格式，便于使用
        flights = []
        for state in data['states']:
            flight = {
                'icao24': state[0],           # ICAO 24位地址
                'callsign': state[1].strip(), # 呼号
                'origin_country': state[2],   # 原产国
                'time_position': state[3],    # 位置更新时间戳
                'last_contact': state[4],     # 最后联系时间
                'longitude': state[5],        # 经度
                'latitude': state[6],         # 纬度
                'baro_altitude': state[7],    # 气压高度（米）
                'on_ground': state[8],        # 是否在地面
                'velocity': state[9],         # 速度（米/秒）
                'true_track': state[10],      # 真实航向（度）
                'vertical_rate': state[11],   # 垂直速度（米/秒）
                'sensors': state[12],         # 传感器
                'geo_altitude': state[13],    # GPS 高度
                'squawk': state[14],          # 应答机代码
                'spi': state[15],             # 特殊位置识别
                'position_source': state[16]  # 位置源
            }
            flights.append(flight)
        
        return flights
    
    def get_aircraft_state(self, icao24: str) -> Optional[Dict]:
        """
        获取特定飞机的实时状态
        
        Args:
            icao24: 飞机的 ICAO 24位地址（16进制，6位字符）
            
        Returns:
            飞机状态字典
        """
        params = {'icao24': icao24.lower()}
        data = self._make_request("states/all", params)
        
        if not data or 'states' not in data or not data['states']:
            return None
        
        # 返回第一个匹配的结果
        state = data['states'][0]
        return {
            'icao24': state[0],
            'callsign': state[1].strip(),
            'origin_country': state[2],
            'longitude': state[5],
            'latitude': state[6],
            'altitude': state[7],
            'on_ground': state[8],
            'velocity': state[9],
            'heading': state[10],
            'vertical_rate': state[11],
            'squawk': state[14]
        }
    
    def get_flights_by_airport(self, airport_icao: str, 
                                arrival: bool = True,
                                departure: bool = False) -> Optional[List[str]]:
        """
        获取机场的到达或出发航班
        
        Args:
            airport_icao: 机场 ICAO 代码（如 ZBAA=北京首都，ZSPD=上海浦东）
            arrival: 是否查询到达航班
            departure: 是否查询出发航班
            
        Returns:
            航班 ICAO 地址列表
        """
        params = {'airport': airport_icao.upper()}
        if arrival:
            endpoint = "flights/arrival"
        elif departure:
            endpoint = "flights/departure"
        else:
            print("❌ 必须指定查询到达或出发航班")
            return None
        
        data = self._make_request(endpoint, params)
        if not data:
            return None
        
        return data
    
    def get_aircraft_tracks(self, icao24: str, 
                            start_time: datetime, 
                            end_time: datetime) -> Optional[List[Dict]]:
        """
        获取飞机的历史轨迹（需要登录账号）
        
        Args:
            icao24: 飞机 ICAO 24位地址
            start_time: 开始时间（UTC）
            end_time: 结束时间（UTC）
            
        Returns:
            轨迹点列表
        """
        if not self.username:
            print("⚠️  查询历史轨迹需要登录账号，请在初始化时提供用户名和密码")
            return None
        
        params = {
            'icao24': icao24.lower(),
            'start': int(start_time.timestamp()),
            'end': int(end_time.timestamp())
        }
        
        data = self._make_request("tracks/all", params)
        if not data:
            return None
        
        return data
    
    def get_my_flights(self, start_time: datetime, end_time: datetime) -> Optional[List[Dict]]:
        """
        获取自己所有航班的历史数据（需要登录账号）
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            航班列表
        """
        if not self.username:
            print("⚠️  此功能需要登录账号")
            return None
        
        params = {
            'begin': int(start_time.timestamp()),
            'end': int(end_time.timestamp())
        }
        
        data = self._make_request("flights/all", params)
        return data


def display_flight_info(flights: List[Dict], limit: int = 10):
    """格式化显示航班信息"""
    if not flights:
        print("没有找到航班数据")
        return
    
    print(f"\n{'='*80}")
    print(f"共找到 {len(flights)} 个航班，显示前 {min(limit, len(flights))} 个:")
    print(f"{'='*80}\n")
    
    print(f"{'呼号':<10} {'国家':<15} {'经纬度':<25} {'高度(m)':<10} {'速度':<10} {'状态'}")
    print("-" * 80)
    
    for i, flight in enumerate(flights[:limit]):
        callsign = flight.get('callsign', 'N/A') or 'N/A'
        country = flight.get('origin_country', 'Unknown')
        lat = flight.get('latitude')
        lon = flight.get('longitude')
        altitude = flight.get('altitude', 'N/A')
        velocity = flight.get('velocity', 'N/A')
        on_ground = "地面" if flight.get('on_ground') else "空中"
        
        if lat is not None and lon is not None:
            position = f"{lat:.4f}, {lon:.4f}"
        else:
            position = "无位置"
        
        altitude_str = str(altitude) if altitude is not None else "N/A"
        velocity_str = f"{velocity:.0f} m/s" if isinstance(velocity, (int, float)) else "N/A"
        
        print(f"{callsign:<10} {country:<15} {position:<25} {altitude_str:<10} {velocity_str:<10} {on_ground}")


def main():
    """主函数 - 使用示例"""
    
    # ==================== 示例 1: 匿名访问（无需账号） ====================
    print("\n🔍 示例 1: 查询北京区域的实时航班（匿名访问）")
    api_anonymous = OpenSkyAPI()
    
    # 北京区域坐标
    flights_beijing = api_anonymous.get_all_states(
        latitude_min=39.5,
        longitude_min=116.0,
        latitude_max=40.5,
        longitude_max=117.0
    )
    
    display_flight_info(flights_beijing, limit=10)
    
    # ==================== 示例 2: 查询特定飞机 ====================
    print("\n\n🔍 示例 2: 查询特定飞机状态")
    # 这里用一个示例 ICAO 码（实际使用时需要替换为真实的）
    # 你可以从上面的结果中找一个真实的 ICAO24 码
    if flights_beijing and len(flights_beijing) > 0:
        sample_icao = flights_beijing[0]['icao24']
        print(f"查询飞机：{sample_icao}")
        aircraft_state = api_anonymous.get_aircraft_state(sample_icao)
        if aircraft_state:
            print(f"  呼号：{aircraft_state['callsign']}")
            print(f"  国家：{aircraft_state['origin_country']}")
            print(f"  位置：{aircraft_state['latitude']}, {aircraft_state['longitude']}")
            print(f"  高度：{aircraft_state['altitude']} 米")
            print(f"  速度：{aircraft_state['velocity']} m/s")
            print(f"  状态：{'地面' if aircraft_state['on_ground'] else '空中'}")
    
    # ==================== 示例 3: 使用认证账号（推荐） ====================
    print("\n\n🔍 示例 3: 使用认证账号访问")
    print("提示：请替换为你的 OpenSky 账号信息")
    
    # 取消注释并填入你的账号来测试
    # YOUR_USERNAME = "your_username"
    # YOUR_PASSWORD = "your_password"
    # api_auth = OpenSkyAPI(username=YOUR_USERNAME, password=YOUR_PASSWORD)
    # 
    # # 查询上海区域航班
    # flights_shanghai = api_auth.get_all_states(
    #     latitude_min=30.5,
    #     longitude_min=120.5,
    #     latitude_max=31.5,
    #     longitude_max=122.0
    # )
    # display_flight_info(flights_shanghai)
    #
    # # 查询历史轨迹（需要登录）
    # if flights_shanghai:
    #     icao = flights_shanghai[0]['icao24']
    #     end_time = datetime.utcnow()
    #     start_time = end_time - timedelta(hours=1)
    #     tracks = api_auth.get_aircraft_tracks(icao, start_time, end_time)
    #     if tracks:
    #         print(f"\n找到 {len(tracks)} 个轨迹点")
    
    # ==================== 示例 4: 查询机场航班 ====================
    print("\n\n🔍 示例 4: 查询机场到达航班")
    print("查询北京首都机场 (ZBAA) 的到达航班...")
    # 注意：此功能也需要登录账号才能获取详细信息
    # flights_arrival = api_auth.get_flights_by_airport("ZBAA", arrival=True)
    
    print("\n" + "="*80)
    print("💡 使用提示:")
    print("  1. 匿名访问限制：约每 10 秒 1 次请求")
    print("  2. 注册用户限制：约每秒 1-2 次请求")
    print("  3. 历史轨迹查询必须使用认证账号")
    print("  4. 注册地址：https://opensky-network.org/register")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
