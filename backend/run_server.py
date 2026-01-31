#!/usr/bin/env python3
"""
航空数据可视化系统服务器启动脚本
使用JSON文件作为数据存储
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # 设置主机和端口
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Starting Aviation Data Visualization Server...")
    print(f"Access the dashboard at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)