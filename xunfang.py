import pandas as pd
import folium
from folium.plugins import HeatMap
import webbrowser
import os
import sys  # pyright: ignore[reportUnusedImport]
import json
from pathlib import Path

# 设置中文字体支持
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

class HeatmapGenerator:
    def __init__(self, excel_path):
        self.excel_path = Path(excel_path)
        self.data = None
        self.map = None
        
    def load_data(self):
        """加载并预处理Excel数据"""
        if not self.excel_path.exists():
            raise FileNotFoundError(f"文件 '{self.excel_path}' 不存在")
            
        df = pd.read_excel(self.excel_path)
        
        # 智能匹配必要列
        column_mapping = {
            '经度': None, '纬度': None, '案发时间': None, '案件类别': None
        }
        
        # 匹配经纬度列
        for col in df.columns:
            col_str = str(col).lower()
            if not column_mapping['经度'] and ('经度' in str(col) or 'lng' in col_str or 'lon' in col_str):
                column_mapping['经度'] = col
            if not column_mapping['纬度'] and ('纬度' in str(col) or 'lat' in col_str):
                column_mapping['纬度'] = col
            if not column_mapping['案发时间'] and ('时间' in str(col) or 'date' in col_str or 'time' in col_str):
                column_mapping['案发时间'] = col
            if not column_mapping['案件类别'] and ('类别' in str(col) or 'type' in col_str or 'category' in col_str):
                column_mapping['案件类别'] = col
        
        # 检查是否找到所有必要列
        missing_cols = [k for k, v in column_mapping.items() if v is None]
        if missing_cols:
            raise ValueError(f"Excel文件缺少必要列: {', '.join(missing_cols)}")
        
        # 重命名列
        df = df.rename(columns={v: k for k, v in column_mapping.items()})
        
        # 数据清洗
        df['案发时间'] = pd.to_datetime(df['案发时间'], errors='coerce')
        df['经度'] = pd.to_numeric(df['经度'], errors='coerce')
        df['纬度'] = pd.to_numeric(df['纬度'], errors='coerce')
        df = df.dropna(subset=['经度', '纬度', '案发时间', '案件类别'])
        df = df[(df['纬度'].between(-90, 90)) & (df['经度'].between(-180, 180))]
        
        self.data = df.to_dict('records')
        return self.data
        
    def create_heatmap(self, output_file='热力图.html'):
        """创建带有筛选功能的热力图"""
        if not self.data:
            raise ValueError("没有可用数据，请先调用load_data()加载数据")
            
        # 提取唯一案件类别和时间范围
        categories = list(set(item['案件类别'] for item in self.data))
        min_date = min(item['案发时间'] for item in self.data).strftime('%Y-%m-%d')
        max_date = max(item['案发时间'] for item in self.data).strftime('%Y-%m-%d')
        
        # 计算地图中心点
        avg_lat = sum(item['纬度'] for item in self.data) / len(self.data)
        avg_lng = sum(item['经度'] for item in self.data) / len(self.data)
        
        # 创建地图对象
        self.map = folium.Map(location=[avg_lat, avg_lng], zoom_start=10, tiles='CartoDB positron')
        
        # 添加筛选控件
        filter_html = f"""
        <div style="position: fixed; top: 10px; left: 10px; z-index: 1000; background-color: white; padding: 15px; border-radius: 5px; box-shadow: 0 1px 5px rgba(0,0,0,0.2);">
            <h3 style="margin-top: 0; font-family: SimHei;">案件筛选</h3>
            <div style="margin-top: 10px;">
                <label style="font-family: SimHei;">案件类别:</label><br>
                {''.join(f'<input type="checkbox" id="cat-{cat}" value="{cat}" checked> <label for="cat-{cat}">{cat}</label><br>' for cat in categories)}
            </div>
            <button onclick="updateHeatmap()" style="margin-top: 10px; padding: 5px 10px; background-color: #0078A8; color: white; border: none; border-radius: 3px; cursor: pointer;">应用筛选</button>
        </div>
        """
        self.map.get_root().html.add_child(folium.Element(filter_html))
        
        # 添加热力图数据和JavaScript逻辑
        # 转换Timestamp为字符串以便JSON序列化
        serializable_data = []
        for item in self.data:
            serializable_item = item.copy()
            serializable_item['案发时间'] = serializable_item['案发时间'].strftime('%Y-%m-%d %H:%M:%S')
            serializable_data.append(serializable_item)
        
        data_js = f"var allData = {json.dumps(serializable_data, ensure_ascii=False)};"
        heatmap_js = f"""
        <script src="https://unpkg.com/leaflet.heat/dist/leaflet-heat.js"></script>
        <script>
            {data_js}
            var map = L.map('map').setView([{avg_lat}, {avg_lng}], 12); // 设定中心和缩放
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {{
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);

            var heatData = allData.map(item => [item.纬度, item.经度, 1]);
            var heat = L.heatLayer(heatData, {{radius: 25, blur: 15}}).addTo(map);
            
            var heatmapLayer;
            
            // 初始化热力图
            function initHeatmap() {{
                var initialData = allData.map(item => [item.纬度, item.经度, 1]);
                heatmapLayer = L.heatLayer(initialData, {{radius: 25, blur: 15}}).addTo(map);
            }}
            
            // 更新热力图数据
            function updateHeatmap() {{
                var selectedCategories = [];
                // 获取选中的类别
                {json.dumps(categories)}.forEach(cat => {{
                    if (document.getElementById('cat-' + cat).checked) {{
                        selectedCategories.push(cat);
                    }}
                }});
                // 筛选数据
                var filteredData = allData.filter(item => selectedCategories.includes(item.案件类别)).map(item => [item.纬度, item.经度, 1]);
                // 更新图层
                if (heatmapLayer) {{
                    map.removeLayer(heatmapLayer);
                }}
                heatmapLayer = L.heatLayer(filteredData, {{radius: 25, blur: 15}}).addTo(map);
            }}
            // 页面加载完成后初始化
            document.addEventListener('DOMContentLoaded', initHeatmap);
        </script>
        """
        self.map.get_root().html.add_child(folium.Element(heatmap_js))
        
        # 保存地图
        self.map.save(output_file)
        return output_file
        
    def run(self, output_file='热力图.html'):
        """运行完整流程: 加载数据并生成热力图"""
        try:
            print(f"正在读取数据: {self.excel_path}")
            self.load_data()
            print(f"成功加载 {len(self.data)} 条记录")
            
            print(f"正在生成热力图...")
            output_path = self.create_heatmap(output_file)
            
            print(f"热力图已生成: {os.path.abspath(output_path)}")
            
            # 尝试打开浏览器
            try:
                webbrowser.open(Path(output_path).as_uri())
            except:
                print("无法自动打开浏览器，请手动打开生成的HTML文件")
        except Exception as e:
            print(f"发生错误: {str(e)}")
            return False
        return True

if __name__ == '__main__':
    # 创建实例并运行 - 使用原始字符串处理Windows路径
    generator = HeatmapGenerator(r'd:\workspace\temp.xlsx')
    generator.run()