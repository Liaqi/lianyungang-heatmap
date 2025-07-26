#!/usr/bin/env python3
"""
快速部署脚本 - 提供互联网访问地址
"""

import os
import json
import webbrowser
from pathlib import Path

class QuickDeployer:
    def __init__(self):
        self.project_name = "lianyungang-heatmap"
        
    def create_mobile_page(self):
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
    </script>
</body>
</html>"""
        
        with open("mobile.html", 'w', encoding='utf-8') as f:
            f.write(mobile_html)
            
        print("✅ 移动端优化页面已创建: mobile.html")
        
    def show_deploy_options(self):
        """显示部署选项"""
        print("\n🌐 连云港市案件热力图 - 互联网部署选项")
        print("=" * 60)
        
        print("\n📋 可用的部署平台:")
        print("1. Vercel (推荐) - 免费、快速、自动HTTPS")
        print("2. Netlify - 免费、功能丰富、CDN加速")
        print("3. GitHub Pages - 免费、与GitHub集成")
        print("4. 本地服务器 - 局域网访问")
        
        print("\n🚀 快速部署步骤:")
        print("=" * 40)
        
        print("\n📦 方法一：Vercel 部署")
        print("1. 访问 https://vercel.com")
        print("2. 使用 GitHub 账号登录")
        print("3. 点击 'New Project'")
        print("4. 导入你的 GitHub 仓库")
        print("5. 点击 'Deploy'")
        print("6. 获得类似 https://your-project.vercel.app 的链接")
        
        print("\n📦 方法二：Netlify 部署")
        print("1. 访问 https://netlify.com")
        print("2. 使用 GitHub 账号登录")
        print("3. 点击 'New site from Git'")
        print("4. 选择你的 GitHub 仓库")
        print("5. 点击 'Deploy site'")
        print("6. 获得类似 https://your-site.netlify.app 的链接")
        
        print("\n📦 方法三：GitHub Pages 部署")
        print("1. 将项目上传到 GitHub")
        print("2. 在仓库设置中启用 GitHub Pages")
        print("3. 选择部署分支 (通常是 main)")
        print("4. 获得类似 https://username.github.io/repository 的链接")
        
        print("\n📦 方法四：本地服务器 (局域网)")
        print("1. 运行: python server.py")
        print("2. 获取本机IP地址")
        print("3. 在手机浏览器访问: http://本机IP:8080")
        
    def create_github_guide(self):
        """创建GitHub部署指南"""
        print("\n📚 GitHub 仓库创建和部署指南")
        print("=" * 50)
        
        print("\n1. 创建 GitHub 仓库")
        print("   - 访问 https://github.com")
        print("   - 点击 'New repository'")
        print("   - 输入仓库名称: lianyungang-heatmap")
        print("   - 选择 'Public' 或 'Private'")
        print("   - 点击 'Create repository'")
        
        print("\n2. 上传项目文件")
        print("   - 在本地项目目录打开命令行")
        print("   - 运行以下命令:")
        print("     git init")
        print("     git add .")
        print("     git commit -m 'Initial commit'")
        print("     git branch -M main")
        print("     git remote add origin https://github.com/你的用户名/lianyungang-heatmap.git")
        print("     git push -u origin main")
        
        print("\n3. 启用 GitHub Pages")
        print("   - 在仓库页面点击 'Settings'")
        print("   - 左侧菜单选择 'Pages'")
        print("   - Source 选择 'Deploy from a branch'")
        print("   - Branch 选择 'main'")
        print("   - 点击 'Save'")
        print("   - 等待几分钟后获得访问链接")
        
        print("\n4. 移动端访问")
        print("   - 获得类似 https://username.github.io/lianyungang-heatmap 的链接")
        print("   - 在手机浏览器中直接访问")
        print("   - 支持触摸操作和手势缩放")
        
    def create_vercel_guide(self):
        """创建Vercel部署指南"""
        print("\n📚 Vercel 部署详细指南")
        print("=" * 40)
        
        print("\n1. 准备工作")
        print("   - 确保项目已上传到 GitHub")
        print("   - 确保项目包含以下文件:")
        print("     - index.html")
        print("     - data.json")
        print("     - vercel.json")
        print("     - mobile.html")
        
        print("\n2. 部署步骤")
        print("   - 访问 https://vercel.com")
        print("   - 使用 GitHub 账号登录")
        print("   - 点击 'New Project'")
        print("   - 选择你的 GitHub 仓库")
        print("   - 保持默认设置，点击 'Deploy'")
        print("   - 等待部署完成")
        
        print("\n3. 配置说明")
        print("   - Framework Preset: Other")
        print("   - Build Command: 留空")
        print("   - Output Directory: .")
        print("   - Install Command: 留空")
        
        print("\n4. 移动端访问")
        print("   - 主页面: https://your-project.vercel.app")
        print("   - 移动端: https://your-project.vercel.app/mobile.html")
        print("   - 支持PWA功能，可添加到主屏幕")
        
    def create_local_server_guide(self):
        """创建本地服务器指南"""
        print("\n📚 本地服务器部署指南")
        print("=" * 40)
        
        print("\n1. 启动本地服务器")
        print("   python server.py")
        
        print("\n2. 获取本机IP地址")
        print("   Windows: ipconfig")
        print("   Mac/Linux: ifconfig 或 ip addr")
        
        print("\n3. 局域网访问")
        print("   - 确保手机和电脑在同一WiFi网络")
        print("   - 在手机浏览器输入: http://本机IP:8080")
        print("   - 例如: http://192.168.1.100:8080")
        
        print("\n4. 移动端优化")
        print("   - 访问 http://本机IP:8080/mobile.html")
        print("   - 支持触摸操作和手势缩放")
        print("   - 可添加到手机主屏幕")
        
        print("\n5. 端口转发 (外网访问)")
        print("   - 在路由器设置中配置端口转发")
        print("   - 将8080端口转发到本机IP")
        print("   - 获取公网IP地址")
        print("   - 外网访问: http://公网IP:8080")
        
    def create_qr_code_guide(self):
        """创建二维码分享指南"""
        print("\n📱 二维码分享指南")
        print("=" * 30)
        
        print("\n1. 生成二维码")
        print("   - 访问 https://qr-code-generator.com")
        print("   - 输入你的网站链接")
        print("   - 下载二维码图片")
        
        print("\n2. 分享方式")
        print("   - 打印二维码贴在墙上")
        print("   - 通过微信、QQ等社交软件分享")
        print("   - 制作成名片或宣传单")
        
        print("\n3. 移动端优化")
        print("   - 确保网站支持移动端访问")
        print("   - 测试触摸操作是否正常")
        print("   - 检查地图缩放功能")
        
    def run(self):
        """运行部署指南"""
        self.create_mobile_page()
        self.show_deploy_options()
        
        print("\n请选择要查看的详细指南:")
        print("1. GitHub 仓库创建指南")
        print("2. Vercel 部署指南")
        print("3. 本地服务器指南")
        print("4. 二维码分享指南")
        print("5. 退出")
        
        while True:
            choice = input("\n请输入选择 (1-5): ").strip()
            
            if choice == "1":
                self.create_github_guide()
            elif choice == "2":
                self.create_vercel_guide()
            elif choice == "3":
                self.create_local_server_guide()
            elif choice == "4":
                self.create_qr_code_guide()
            elif choice == "5":
                print("退出部署指南")
                break
            else:
                print("无效选择，请重新输入")
                
        print("\n🎉 部署指南完成！")
        print("选择你喜欢的部署方式，按照指南操作即可。")
        print("部署完成后，你就可以在互联网上访问热力图了！")

if __name__ == "__main__":
    deployer = QuickDeployer()
    deployer.run() 