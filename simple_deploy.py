#!/usr/bin/env python3
"""
简化部署脚本
支持多种部署方式
"""

import os
import sys
import json
import webbrowser
from pathlib import Path

class SimpleDeployer:
    def __init__(self):
        self.project_name = "lianyungang-heatmap"
        
    def create_deploy_files(self):
        """创建部署所需的文件"""
        
        # 创建 package.json
        package_json = {
            "name": self.project_name,
            "version": "1.0.0",
            "description": "连云港市案件热力图分析系统",
            "main": "index.html",
            "scripts": {
                "start": "python server.py",
                "build": "echo 'No build step required'",
                "deploy": "echo 'Deploy to your preferred platform'"
            },
            "keywords": ["heatmap", "lianyungang", "crime-analysis"],
            "author": "Your Name",
            "license": "MIT"
        }
        
        with open("package.json", 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
            
        print("✅ package.json 已创建")
        
        # 创建 .gitignore
        gitignore_content = """
# 系统文件
.DS_Store
Thumbs.db

# 日志文件
*.log

# 临时文件
*.tmp
*.temp

# 环境文件
.env
.env.local

# 依赖目录
node_modules/
__pycache__/
*.pyc

# 部署文件
.vercel/
.netlify/
dist/
build/
        """.strip()
        
        with open(".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
            
        print("✅ .gitignore 已创建")
        
    def show_deploy_options(self):
        """显示部署选项"""
        print("\n🌐 连云港市案件热力图 - 互联网部署选项")
        print("=" * 60)
        
        print("\n📋 可用的部署平台:")
        print("1. Vercel (推荐) - 免费、快速、自动HTTPS")
        print("2. Netlify - 免费、功能丰富、CDN加速")
        print("3. GitHub Pages - 免费、与GitHub集成")
        print("4. 云服务器 - 完全控制、自定义域名")
        print("5. 本地服务器 - 局域网访问")
        
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
        
        print("\n📦 方法四：云服务器部署")
        print("1. 购买云服务器 (阿里云、腾讯云等)")
        print("2. 上传项目文件到服务器")
        print("3. 安装 Nginx 或 Apache")
        print("4. 配置域名解析")
        print("5. 获得自定义域名访问")
        
        print("\n📦 方法五：本地服务器 (局域网)")
        print("1. 运行: python server.py")
        print("2. 获取本机IP地址")
        print("3. 在手机浏览器访问: http://本机IP:8080")
        
    def create_github_repo_guide(self):
        """创建GitHub仓库指南"""
        print("\n📚 GitHub 仓库创建指南")
        print("=" * 40)
        
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
        
        print("\n4. 自定义域名 (可选)")
        print("   - 在项目设置中添加自定义域名")
        print("   - 配置DNS解析")
        print("   - 等待SSL证书生效")
        
    def create_netlify_guide(self):
        """创建Netlify部署指南"""
        print("\n📚 Netlify 部署详细指南")
        print("=" * 40)
        
        print("\n1. 准备工作")
        print("   - 确保项目已上传到 GitHub")
        print("   - 确保项目包含 netlify.toml 文件")
        
        print("\n2. 部署步骤")
        print("   - 访问 https://netlify.com")
        print("   - 使用 GitHub 账号登录")
        print("   - 点击 'New site from Git'")
        print("   - 选择 GitHub")
        print("   - 选择你的仓库")
        print("   - 保持默认设置，点击 'Deploy site'")
        
        print("\n3. 配置说明")
        print("   - Build command: 留空")
        print("   - Publish directory: .")
        print("   - 其他设置保持默认")
        
        print("\n4. 功能配置")
        print("   - 在 'Site settings' 中配置重定向")
        print("   - 在 'Domain management' 中添加自定义域名")
        print("   - 在 'Forms' 中查看表单提交")
        
    def show_local_server_guide(self):
        """显示本地服务器指南"""
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
        
        print("\n4. 端口转发 (外网访问)")
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
        self.create_deploy_files()
        self.show_deploy_options()
        
        print("\n请选择要查看的详细指南:")
        print("1. GitHub 仓库创建指南")
        print("2. Vercel 部署指南")
        print("3. Netlify 部署指南")
        print("4. 本地服务器指南")
        print("5. 二维码分享指南")
        print("6. 退出")
        
        while True:
            choice = input("\n请输入选择 (1-6): ").strip()
            
            if choice == "1":
                self.create_github_repo_guide()
            elif choice == "2":
                self.create_vercel_guide()
            elif choice == "3":
                self.create_netlify_guide()
            elif choice == "4":
                self.show_local_server_guide()
            elif choice == "5":
                self.create_qr_code_guide()
            elif choice == "6":
                print("退出部署指南")
                break
            else:
                print("无效选择，请重新输入")
                
        print("\n🎉 部署指南完成！")
        print("选择你喜欢的部署方式，按照指南操作即可。")
        print("部署完成后，你就可以在互联网上访问热力图了！")

if __name__ == "__main__":
    deployer = SimpleDeployer()
    deployer.run() 