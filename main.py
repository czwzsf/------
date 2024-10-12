import os
import re
import pandas as pd

# 文件地址
path = 'data/Data_JH6'

# 初始化一个空的列表来存储文件信息
data = []

# 定义已知的车型
known_models = ['JH6', 'JH5', '悍V', '龙V', '鹰途']

# 遍历文件夹中的所有文件
for filename in os.listdir(path):
    if filename.endswith('.docx'):
        # 使用正则表达式分割文件名，考虑不同类型的破折号
        parts = re.split(r'[-–—]', filename)
        if len(parts) >= 6:
            # 获取车型平台与品系
            car_model = parts[4]
            # 初始化车型和品系
            vehicle_model = None
            series = None
            # 检查车型平台字段是否包含已知车型
            for model in known_models:
                if model in car_model:
                    vehicle_model = model
                    series = car_model.split(model, 1)[1]
                    break
            # 将信息添加到列表中
            if vehicle_model and series:
                data.append([vehicle_model, series])

# 将列表转换为DataFrame
df = pd.DataFrame(data, columns=['车型', '品系'])

# 打印DataFrame
print(df)
