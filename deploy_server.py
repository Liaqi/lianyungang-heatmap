#!/usr/bin/env python3
"""
云服务器部署脚本
支持多种云服务商部署
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class CloudDeployer:
    def __init__(self):
        self.project_name = "lianyungang-heatmap"
        self.config_file = "deploy_config.json"
        
    def create_deploy_config(self):
        """创建部署配置文件"""
        config = {
            "project_name": self.project_name,
            "deploy_methods": {
                "vercel": {
                    "enabled": True,
                    "command": "vercel --prod"
                },
                "netlify": {
                    "enabled": True,
                    "command": "netlify deploy --prod"
                },
                "github_pages": {
                    "enabled": True,
                    "command": "gh-pages -d ."
                }
            },
            "files_to_deploy": [
                "index.html",
                "data.json",
                "*.css",
                "*.js",
                "*.md"
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        print(f"部署配置文件已创建: {self.config_file}")
        
    def deploy_to_vercel(self):
        """部署到Vercel"""
        print("正在部署到Vercel...")
        try:
            # 检查是否安装了Vercel CLI
            result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Vercel CLI未安装，正在安装...")
                subprocess.run(["npm", "install", "-g", "vercel"], check=True)
            
            # 部署到Vercel
            result = subprocess.run(["vercel", "--prod"], check=True)
            print("✅ Vercel部署成功！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Vercel部署失败: {e}")
            return False
            
    def deploy_to_netlify(self):
        """部署到Netlify"""
        print("正在部署到Netlify...")
        try:
            # 检查是否安装了Netlify CLI
            result = subprocess.run(["netlify", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Netlify CLI未安装，正在安装...")
                subprocess.run(["npm", "install", "-g", "netlify-cli"], check=True)
            
            # 部署到Netlify
            result = subprocess.run(["netlify", "deploy", "--prod"], check=True)
            print("✅ Netlify部署成功！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Netlify部署失败: {e}")
            return False
            
    def deploy_to_github_pages(self):
        """部署到GitHub Pages"""
        print("正在部署到GitHub Pages...")
        try:
            # 检查是否安装了gh-pages
            result = subprocess.run(["npx", "gh-pages", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("gh-pages未安装，正在安装...")
                subprocess.run(["npm", "install", "-g", "gh-pages"], check=True)
            
            # 部署到GitHub Pages
            result = subprocess.run(["npx", "gh-pages", "-d", "."], check=True)
            print("✅ GitHub Pages部署成功！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ GitHub Pages部署失败: {e}")
            return False
            
    def create_package_json(self):
        """创建package.json文件"""
        package_json = {
            "name": self.project_name,
            "version": "1.0.0",
            "description": "连云港市案件热力图分析系统",
            "main": "index.html",
            "scripts": {
                "start": "python server.py",
                "deploy": "python deploy_server.py",
                "deploy:vercel": "vercel --prod",
                "deploy:netlify": "netlify deploy --prod",
                "deploy:github": "gh-pages -d ."
            },
            "keywords": ["heatmap", "lianyungang", "crime-analysis"],
            "author": "Your Name",
            "license": "MIT",
            "devDependencies": {
                "gh-pages": "^5.0.0"
            }
        }
        
        with open("package.json", 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
            
        print("package.json文件已创建")
        
    def run(self):
        """运行部署脚本"""
        print("🌐 连云港市案件热力图 - 互联网部署工具")
        print("=" * 50)
        
        # 创建必要的配置文件
        self.create_deploy_config()
        self.create_package_json()
        
        print("\n请选择部署方式:")
        print("1. Vercel (推荐)")
        print("2. Netlify")
        print("3. GitHub Pages")
        print("4. 全部部署")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == "1":
            self.deploy_to_vercel()
        elif choice == "2":
            self.deploy_to_netlify()
        elif choice == "3":
            self.deploy_to_github_pages()
        elif choice == "4":
            print("正在部署到所有平台...")
            self.deploy_to_vercel()
            self.deploy_to_netlify()
            self.deploy_to_github_pages()
        elif choice == "5":
            print("退出部署")
            return
        else:
            print("无效选择")
            
        print("\n部署完成！请查看上述输出获取访问链接。")

if __name__ == "__main__":
    deployer = CloudDeployer()
    deployer.run() 