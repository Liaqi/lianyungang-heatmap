import pandas as pd
import folium
from folium.plugins import HeatMap
import webbrowser
import os
import sys
from pathlib import Path

# 设置中文字体支持
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

def load_excel_data(file_path):
    """加载Excel文件并提取经纬度数据"""
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 检查必要的列是否存在
        required_columns = ['经度', '纬度']
        if not all(col in df.columns for col in required_columns):
            # 尝试寻找可能的列名变体
            lat_cols = [col for col in df.columns if '纬度' in str(col) or 'lat' in str(col).lower()]
            lng_cols = [col for col in df.columns if '经度' in str(col) or 'lng' in str(col).lower() or 'lon' in str(col).lower()]
            
            if not lat_cols or not lng_cols:
                raise ValueError("未找到经纬度列，请确保Excel中包含'经度'和'纬度'列")
                
            df = df.rename(columns={lat_cols[0]: '纬度', lng_cols[0]: '经度'})
        
        # 过滤无效数据
        df = df.dropna(subset=['经度', '纬度'])
        df = df[(df['纬度'].between(-90, 90)) & (df['经度'].between(-180, 180))]
        
        return df[['经度', '纬度']].values.tolist()
        
    except Exception as e:
        print(f"数据加载错误: {str(e)}")
        return []

def create_heatmap_html(coordinates, output_file='heatmap.html'):
    """创建热点图HTML文件"""
    if not coordinates:
        print("没有可用的坐标数据，无法生成热点图")
        return False
    
    # 计算地图中心点（使用所有坐标的平均值）
    avg_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
    avg_lng = sum(coord[0] for coord in coordinates) / len(coordinates)
    
    # 创建地图对象
    m = folium.Map(location=[avg_lat, avg_lng], zoom_start=10, tiles='CartoDB positron')
    
    # 添加热力图图层
    HeatMap(coordinates, radius=15, blur=10).add_to(m)
    
    # 添加标题和说明
    title_html = '''<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 1000; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0 1px 5px rgba(0,0,0,0.2);">
                    <h3 style="margin: 0; font-family: SimHei, Arial; color: #333;">案件数据热点图</h3>
                    <p style="margin: 5px 0 0; font-family: SimHei, Arial; font-size: 12px; color: #666;">共{count}个数据点</p>
                  </div>'''.format(count=len(coordinates))
    m.get_root().html.add_child(folium.Element(title_html))
    
    # 保存地图为HTML文件
    m.save(output_file)
    return True

def main():
    # Excel文件路径 - 修改为用户指定的temp.xlsx
    excel_path = Path('d:\workspace\temp.xlsx')
    
    # 检查文件是否存在
    if not excel_path.exists():
        print(f"错误: 文件 '{excel_path}' 不存在")
        return
    
    print(f"正在读取数据: {excel_path}")
    coordinates = load_excel_data(excel_path)
    
    if not coordinates:
        print("未能提取有效的经纬度数据")
        return
    
    print(f"成功提取 {len(coordinates)} 个坐标点")
    
    # 生成热点图HTML
    output_html = '案件热点图.html'
    if create_heatmap_html(coordinates, output_html):
        # 获取绝对路径并处理Windows兼容性
        abs_path = os.path.abspath(output_html)
        print(f"热点图已生成: {abs_path}")
        
        # 方法1：使用pathlib生成标准file URL（推荐）
        try:
            file_url = Path(abs_path).as_uri()
            print(f"尝试打开: {file_url}")
            if webbrowser.open(file_url):
                print("方法1成功: 使用webbrowser.open打开URL")
                return
        except Exception as e1:
            print(f"方法1失败: {str(e1)}")
        
        # 方法2：使用Windows系统命令（备用）
        try:
            # 使用start命令打开文件
            os.startfile(abs_path)
            print("方法2成功: 使用os.startfile打开文件")
            return
        except Exception as e2:
            print(f"方法2失败: {str(e2)}")
        
        # 方法3：手动构造兼容Windows的URL（最终方案）
        try:
            # 处理Windows路径分隔符和驱动器号
            win_url = f"file:///{abs_path.replace(os.sep, '/')}"
            print(f"尝试打开兼容URL: {win_url}")
            if webbrowser.open(win_url):
                print("方法3成功: 使用兼容URL打开")
                return
        except Exception as e3:
            print(f"方法3失败: {str(e3)}")
        
        # 所有方法失败时提供手动指引
        print("\n所有自动打开方法均失败，请手动操作：")
        print(f"1. 打开文件资源管理器")
        print(f"2. 导航到: {os.path.dirname(abs_path)}")
        print(f"3. 双击文件: {os.path.basename(abs_path)}")
        
        # 自动打开浏览器查看
        if sys.platform.startswith('win'):
            # 指定Windows默认浏览器路径（根据实际情况调整）
            browser_path = 'C:/Users/lijia/AppData/Local/Google/Chrome/Application/chrome.exe'
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(browser_path))
            webbrowser.get('chrome').open(output_html)
        else:
            webbrowser.open(output_html)
if __name__ == '__main__':
    main()
