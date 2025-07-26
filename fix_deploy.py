#!/usr/bin/env python3
"""
修复部署问题脚本
"""

import os
import shutil
import subprocess
import sys

def fix_vercel_config():
    """修复Vercel配置文件"""
    print("🔧 修复Vercel配置文件...")
    
    # 备份原配置文件
    if os.path.exists("vercel.json"):
        shutil.copy("vercel.json", "vercel.json.backup")
        print("✅ 已备份原配置文件: vercel.json.backup")
    
    # 使用简化的配置文件
    if os.path.exists("vercel-simple.json"):
        shutil.copy("vercel-simple.json", "vercel.json")
        print("✅ 已应用简化的Vercel配置")
    
    # 验证配置文件
    try:
        import json
        with open("vercel.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查是否同时存在builds和functions
        if "builds" in config and "functions" in config:
            print("❌ 配置文件中同时存在builds和functions属性")
            # 移除functions属性
            if "functions" in config:
                del config["functions"]
                with open("vercel.json", 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                print("✅ 已移除functions属性")
        else:
            print("✅ Vercel配置文件验证通过")
            
    except Exception as e:
        print(f"❌ 配置文件验证失败: {e}")

def check_requirements():
    """检查部署要求"""
    print("\n📋 检查部署要求...")
    
    required_files = [
        "index.html",
        "mobile.html", 
        "data.json",
        "vercel.json",
        "package.json"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - 缺失")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  缺失文件: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ 所有必需文件已准备就绪")
        return True

def create_minimal_vercel_config():
    """创建最小化的Vercel配置"""
    print("\n📝 创建最小化Vercel配置...")
    
    minimal_config = {
        "version": 2,
        "name": "lianyungang-heatmap",
        "builds": [
            {
                "src": "*.html",
                "use": "@vercel/static"
            },
            {
                "src": "*.json",
                "use": "@vercel/static"
            }
        ],
        "routes": [
            {
                "src": "/",
                "dest": "/index.html"
            },
            {
                "src": "/mobile",
                "dest": "/mobile.html"
            }
        ]
    }
    
    import json
    with open("vercel.json", 'w', encoding='utf-8') as f:
        json.dump(minimal_config, f, indent=2, ensure_ascii=False)
    
    print("✅ 已创建最小化Vercel配置")

def deploy_to_vercel():
    """部署到Vercel"""
    print("\n🚀 开始部署到Vercel...")
    
    try:
        # 检查是否已安装Vercel CLI
        result = subprocess.run("vercel --version", shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Vercel CLI未安装，正在安装...")
            subprocess.run("npm install -g vercel", shell=True, check=True)
            print("✅ Vercel CLI安装完成")
        
        # 部署项目
        print("📤 正在部署项目...")
        deploy_result = subprocess.run("vercel --prod --yes", shell=True, capture_output=True, text=True)
        
        if deploy_result.returncode == 0:
            print("✅ 部署成功！")
            
            # 尝试从输出中提取URL
            output = deploy_result.stdout
            if "https://" in output:
                lines = output.split('\n')
                for line in lines:
                    if "https://" in line and ".vercel.app" in line:
                        url = line.strip()
                        print(f"\n🌐 部署地址: {url}")
                        print(f"📱 移动端地址: {url}/mobile.html")
                        return url
            
            print("✅ 部署完成，请检查Vercel控制台获取访问地址")
            return "部署成功"
        else:
            print(f"❌ 部署失败: {deploy_result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 部署过程中出现错误: {e}")
        return None

def show_deployment_guide():
    """显示部署指南"""
    print("\n📚 手动部署指南")
    print("=" * 50)
    
    print("\n1. 访问 https://vercel.com")
    print("2. 使用GitHub账号登录")
    print("3. 点击 'New Project'")
    print("4. 导入你的GitHub仓库")
    print("5. 保持默认设置，点击 'Deploy'")
    print("6. 等待部署完成")
 
    print("\n📱 移动端访问")
    print("- 主页面: https://your-project.vercel.app")
    print("- 移动端: https://your-project.vercel.app/mobile.html")
    
    print("\n🔧 如果仍有问题，请检查:")
    print("- 确保所有文件已上传到GitHub")
    print("- 确保vercel.json配置正确")
    print("- 检查Vercel控制台的错误信息")

def main():
    """主函数"""
    print("🔧 连云港市案件热力图 - 部署问题修复工具")
    print("=" * 60)
    
    # 修复Vercel配置
    fix_vercel_config()
    
    # 检查要求
    if not check_requirements():
        print("\n❌ 部署要求未满足，请确保所有必需文件存在")
        return
    
    # 创建最小化配置
    create_minimal_vercel_config()
    
    print("\n请选择操作:")
    print("1. 自动部署到Vercel")
    print("2. 查看手动部署指南")
    print("3. 退出")
    
    while True:
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            url = deploy_to_vercel()
            if url:
                print(f"\n🎉 部署成功！访问地址: {url}")
                print(f"📱 移动端地址: {url}/mobile.html")
            break
        elif choice == "2":
            show_deployment_guide()
            break
        elif choice == "3":
            print("退出修复工具")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 