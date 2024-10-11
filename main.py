import os
import pandas as pd
import re

# 文件地址
path = 'data/Data_JH6'

# 初始化一个空的列表来存储文件信息
data = []

# 遍历文件夹中的所有文件
for filename in os.listdir(path):
    if filename.endswith('.docx'):
        # 使用正则表达式替换所有的文字版本的“-”为数字版本的“-”
        filename = re.sub(r'－', '-', filename)
        # 使用正则表达式匹配车型平台与品系和车辆底盘号与方案号
        match = re.search(r'-(\w+)-(\w+)\((\w+)\)', filename)
        if match:
            # 获取车型平台与品系
            car_model = match.group(1)
            # 获取车辆底盘号
            chassis_number = match.group(2)
            # 获取方案号
            scheme_number = match.group(3)
            # 将信息添加到列表中
            data.append([car_model, chassis_number, scheme_number])

# 将列表转换为DataFrame
df = pd.DataFrame(data, columns=['车型平台与品系', '车辆底盘号', '方案号'])

# 打印DataFrame
print(df)