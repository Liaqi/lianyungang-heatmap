import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('temp.xlsx')

# 显示基本信息
print("数据形状:", df.shape)
print("\n列名:")
print(df.columns.tolist())
print("\n前5行数据:")
print(df.head())
print("\n数据类型:")
print(df.dtypes)
print("\n数据统计:")
print(df.describe())

# 如果有案件类别列，显示类别分布
if '案件类别' in df.columns:
    print("\n案件类别分布:")
    print(df['案件类别'].value_counts())

# 保存为JSON格式以便前端使用
df.to_json('data.json', orient='records', force_ascii=False, indent=2)
print("\n数据已保存为 data.json") 