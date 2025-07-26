import http.server
import socketserver
import os
import webbrowser
import ssl
import socket
from urllib.parse import urlparse
import json

class MobileHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加移动端优化的HTTP头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        # 移动端优化
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # 自定义日志格式
        print(f"[{self.log_date_time_string()}] {format % args}")

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 连接到外部地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def find_available_port(start_port=8000, max_attempts=10):
    """查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def start_mobile_server(port=None):
    """启动移动端优化的HTTP服务器"""
    handler = MobileHTTPRequestHandler
    
    # 如果没有指定端口，查找可用端口
    if port is None:
        port = find_available_port(8001)  # 从8001开始，避免与8000冲突
        if port is None:
            print("错误：无法找到可用端口")
            return
    
    # 获取本机IP
    local_ip = get_local_ip()
    
    print("=" * 50)
    print("连云港市案件热力图 - 移动端服务器")
    print("=" * 50)
    print(f"本机IP地址: {local_ip}")
    print(f"HTTP服务器: http://{local_ip}:{port}")
    print(f"移动端访问: http://{local_ip}:{port}")
    print("=" * 50)
    print("移动端使用说明:")
    print("1. 确保手机和电脑在同一WiFi网络")
    print("2. 在手机浏览器中输入上述地址")
    print("3. 支持触摸操作、手势缩放等")
    print("4. 点击左上角菜单按钮进行筛选")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            print(f"服务器启动在端口 {port}")
            print("按 Ctrl+C 停止服务器")
            
            # 自动打开浏览器
            webbrowser.open(f'http://localhost:{port}')
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n服务器已停止")
    except OSError as e:
        print(f"错误：无法启动服务器在端口 {port}")
        print(f"错误信息：{e}")
        print("尝试使用其他端口...")
        # 尝试其他端口
        alt_port = find_available_port(port + 1)
        if alt_port:
            print(f"尝试使用端口 {alt_port}")
            start_mobile_server(alt_port)
        else:
            print("无法找到可用端口，请检查网络设置")

def create_mobile_config():
    """创建移动端配置文件"""
    config = {
        "mobile_optimized": True,
        "touch_enabled": True,
        "gesture_support": True,
        "responsive_design": True,
        "offline_support": False,
        "cache_strategy": "no-cache"
    }
    
    with open('mobile_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("移动端配置文件已创建: mobile_config.json")

if __name__ == "__main__":
    # 创建移动端配置
    create_mobile_config()
    
    # 启动服务器
    start_mobile_server() 