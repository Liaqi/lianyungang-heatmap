#!/usr/bin/env python3
"""
自动部署到互联网并输出移动端访问地址
"""

import os
import sys
import json
import subprocess
import webbrowser
from pathlib import Path

class InternetDeployer:
    def __init__(self):
        self.project_name = "lianyungang-heatmap"
        self.deploy_url = None
        
    def check_requirements(self):
        """检查部署要求"""
        print("🔍 检查部署要求...")
        
        required_files = [
            "index.html",
            "data.json",
            "vercel.json",
            "package.json"
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
                
        if missing_files:
            print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
            return False
            
        print("✅ 所有必要文件已存在")
        return True
        
    def install_vercel_cli(self):
        """安装Vercel CLI"""
        print("📦 检查Vercel CLI...")
        
        try:
            # 检查是否已安装
            result = subprocess.run(["vercel", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Vercel CLI 已安装")
                return True
        except FileNotFoundError:
            pass
            
        print("📥 正在安装Vercel CLI...")
        try:
            # 安装Vercel CLI
            subprocess.run(["npm", "install", "-g", "vercel"], check=True)
            print("✅ Vercel CLI 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Vercel CLI 安装失败: {e}")
            return False
            
    def deploy_to_vercel(self):
        """部署到Vercel"""
        print("🚀 正在部署到Vercel...")
        
        try:
            # 登录Vercel（如果需要）
            print("🔐 检查Vercel登录状态...")
            login_result = subprocess.run(["vercel", "whoami"], 
                                        capture_output=True, text=True)
            
            if login_result.returncode != 0:
                print("🔐 需要登录Vercel，请在浏览器中完成登录...")
                subprocess.run(["vercel", "login"], check=True)
            
            # 部署项目
            print("📤 正在部署项目...")
            deploy_result = subprocess.run(["vercel", "--prod", "--yes"], 
                                         capture_output=True, text=True)
            
            if deploy_result.returncode == 0:
                # 解析部署URL
                output = deploy_result.stdout
                for line in output.split('\n'):
                    if 'https://' in line and '.vercel.app' in line:
                        self.deploy_url = line.strip()
                        break
                        
                if self.deploy_url:
                    print(f"✅ 部署成功！")
                    print(f"🌐 访问地址: {self.deploy_url}")
                    return True
                else:
                    print("❌ 无法获取部署URL")
                    return False
            else:
                print(f"❌ 部署失败: {deploy_result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 部署过程出错: {e}")
            return False
            
    def create_mobile_optimized_page(self):
        """创建移动端优化页面"""
        print("📱 创建移动端优化页面...")
        
        mobile_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>连云港市案件热力图 - 移动端</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            overflow: hidden;
        }
        
        .mobile-container {
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .mobile-header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        
        .mobile-header h1 {
            font-size: 18px;
            color: #333;
            margin-bottom: 5px;
        }
        
        .mobile-header p {
            font-size: 12px;
            color: #666;
        }
        
        .map-container {
            flex: 1;
            position: relative;
        }
        
        #map {
            width: 100% !important;
            height: 100% !important;
        }
        
        .mobile-controls {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 1000;
        }
        
        .mobile-btn {
            background: rgba(255, 255, 255, 0.9);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
            cursor: pointer;
            touch-action: manipulation;
        }
        
        .loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            z-index: 2000;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
</head>
<body>
    <div class="mobile-container">
        <div class="mobile-header">
            <h1>连云港市案件热力图</h1>
            <p>移动端优化版本</p>
        </div>
        
        <div class="map-container">
            <div id="map"></div>
            
            <div class="mobile-controls">
                <button class="mobile-btn" onclick="toggleFullscreen()">⛶</button>
                <button class="mobile-btn" onclick="refreshMap()">🔄</button>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div>正在加载地图...</div>
            </div>
        </div>
    </div>

    <script>
        let map;
        let heatmapLayer;
        let isMobile = window.innerWidth <= 768;
        
        // 连云港市边界
        const lianyungangBounds = [
            [34.5, 119.0],  // 西南角
            [34.8, 119.4]   // 东北角
        ];
        
        function initMap() {
            try {
                map = L.map('map', {
                    center: [34.6109, 119.2153],
                    zoom: isMobile ? 11 : 12,
                    minZoom: 10,
                    maxZoom: 18,
                    tap: true,
                    tapTolerance: 15,
                    zoomControl: true,
                    attributionControl: true
                });
                
                // 使用可靠的地图源
                const layer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors',
                    maxZoom: 19,
                    subdomains: 'abc'
                });
                
                layer.on('load', function() {
                    console.log('地图加载成功');
                    hideLoading();
                });
                
                layer.on('tileerror', function(e) {
                    console.error('地图瓦片加载失败:', e);
                });
                
                layer.addTo(map);
                
                // 设置地图边界
                map.setMaxBounds(lianyungangBounds);
                
                // 移动端优化
                if (isMobile) {
                    map.doubleClickZoom.disable();
                    
                    // 优化触摸操作
                    map.on('touchstart', function() {
                        // 触摸开始时的处理
                    });
                }
                
                // 加载数据
                loadData();
                
            } catch (error) {
                console.error('地图初始化错误:', error);
                hideLoading();
                alert('地图初始化失败，请刷新页面重试');
            }
        }
        
        function loadData() {
            fetch('data.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('数据加载失败');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('数据加载成功:', data.length, '条记录');
                    createHeatmap(data);
                })
                .catch(error => {
                    console.error('数据加载错误:', error);
                    alert('数据加载失败，请检查网络连接');
                });
        }
        
        function createHeatmap(data) {
            try {
                // 转换数据格式
                const heatmapData = data.map(item => [
                    parseFloat(item.纬度),
                    parseFloat(item.经度),
                    1  // 权重
                ]).filter(point => 
                    !isNaN(point[0]) && !isNaN(point[1]) &&
                    point[0] >= lianyungangBounds[0][0] && point[0] <= lianyungangBounds[1][0] &&
                    point[1] >= lianyungangBounds[0][1] && point[1] <= lianyungangBounds[1][1]
                );
                
                console.log('有效数据点:', heatmapData.length);
                
                if (heatmapData.length > 0) {
                    // 创建热力图
                    heatmapLayer = L.heatLayer(heatmapData, {
                        radius: 25,
                        blur: 15,
                        maxZoom: 10,
                        gradient: {
                            0.4: 'blue',
                            0.6: 'lime',
                            0.8: 'orange',
                            1.0: 'red'
                        }
                    }).addTo(map);
                    
                    console.log('热力图创建成功');
                } else {
                    console.warn('没有有效的数据点');
                }
                
            } catch (error) {
                console.error('热力图创建错误:', error);
            }
        }
        
        function hideLoading() {
            const loading = document.getElementById('loading');
            if (loading) {
                loading.style.display = 'none';
            }
        }
        
        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }
        
        function refreshMap() {
            if (map) {
                map.invalidateSize();
                if (heatmapLayer) {
                    map.removeLayer(heatmapLayer);
                    loadData();
                }
            }
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            console.log('页面加载完成，开始初始化地图...');
            initMap();
        });
        
        // 窗口大小改变时重新调整地图
        window.addEventListener('resize', function() {
            if (map) {
                setTimeout(() => {
                    map.invalidateSize();
                }, 100);
            }
        });
        
        // 错误处理
        window.addEventListener('error', function(e) {
            console.error('页面错误:', e.error);
        });
        
        window.addEventListener('unhandledrejection', function(e) {
            console.error('未处理的Promise拒绝:', e.reason);
        });
    </script>
</body>
</html>"""
        
        with open("mobile.html", 'w', encoding='utf-8') as f:
            f.write(mobile_html)
            
        print("✅ 移动端优化页面已创建: mobile.html")
        
    def create_qr_code(self):
        """创建二维码"""
        if not self.deploy_url:
            print("❌ 没有部署URL，无法生成二维码")
            return
            
        print("📱 生成二维码...")
        
        # 创建二维码HTML页面
        qr_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>热力图访问二维码</title>
    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            max-width: 400px;
            margin: 0 auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
        #qrcode {{
            margin: 20px 0;
        }}
        .url {{
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            margin: 20px 0;
            word-break: break-all;
            font-size: 14px;
        }}
        .instructions {{
            text-align: left;
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 10px;
        }}
        .instructions h3 {{
            margin-top: 0;
            color: #333;
        }}
        .instructions ol {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .instructions li {{
            margin: 5px 0;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 连云港市案件热力图</h1>
        <p>扫描二维码访问移动端页面</p>
        
        <div id="qrcode"></div>
        
        <div class="url">
            <strong>访问地址:</strong><br>
            {self.deploy_url}
        </div>
        
        <div class="instructions">
            <h3>📱 移动端使用说明:</h3>
            <ol>
                <li>用手机扫描上方二维码</li>
                <li>在手机浏览器中打开链接</li>
                <li>支持触摸缩放和拖拽</li>
                <li>点击热力点查看详细信息</li>
                <li>可添加到手机主屏幕</li>
            </ol>
        </div>
    </div>

    <script>
        // 生成二维码
        QRCode.toCanvas(document.getElementById('qrcode'), '{self.deploy_url}', {{
            width: 200,
            margin: 2,
            color: {{
                dark: '#000000',
                light: '#FFFFFF'
            }}
        }}, function (error) {{
            if (error) console.error(error);
            console.log('二维码生成成功');
        }});
        
        // 复制链接功能
        function copyUrl() {{
            navigator.clipboard.writeText('{self.deploy_url}').then(function() {{
                alert('链接已复制到剪贴板');
            }});
        }}
    </script>
</body>
</html>"""
        
        with open("qr_code.html", 'w', encoding='utf-8') as f:
            f.write(qr_html)
            
        print("✅ 二维码页面已创建: qr_code.html")
        
    def run(self):
        """运行部署流程"""
        print("🌐 连云港市案件热力图 - 互联网部署")
        print("=" * 50)
        
        # 检查要求
        if not self.check_requirements():
            return
            
        # 创建移动端优化页面
        self.create_mobile_optimized_page()
        
        # 安装Vercel CLI
        if not self.install_vercel_cli():
            print("❌ Vercel CLI 安装失败，请手动安装")
            print("运行: npm install -g vercel")
            return
            
        # 部署到Vercel
        if self.deploy_to_vercel():
            # 创建二维码
            self.create_qr_code()
            
            print("\n🎉 部署完成！")
            print("=" * 50)
            print(f"🌐 主页面: {self.deploy_url}")
            print(f"📱 移动端: {self.deploy_url}/mobile.html")
            print(f"📋 二维码: {self.deploy_url}/qr_code.html")
            
            print("\n📱 移动端访问方式:")
            print("1. 直接访问: " + self.deploy_url)
            print("2. 扫描二维码: " + self.deploy_url + "/qr_code.html")
            print("3. 分享链接给其他人")
            
            # 自动打开二维码页面
            try:
                webbrowser.open(self.deploy_url + "/qr_code.html")
            except:
                pass
                
        else:
            print("❌ 部署失败，请检查网络连接和Vercel账号")

if __name__ == "__main__":
    deployer = InternetDeployer()
    deployer.run() 