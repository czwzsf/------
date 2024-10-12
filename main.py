import os
import re
import pandas as pd

# 文件地址
path = 'data/Data_JH6'

# 初始化一个空的列表来存储文件信息
data = []

# 遍历文件夹中的所有文件
for filename in os.listdir(path):
    if filename.endswith('.docx'):
        # 使用正则表达式分割文件名，考虑不同类型的破折号
        parts = re.split(r'[-–—]', filename)
        if len(parts) >= 6:
            # 获取车型平台与品系
            car_model = parts[4]
            # 将信息添加到列表中
            data.append([car_model])

# 将列表转换为DataFrame
df = pd.DataFrame(data, columns=['车型平台与品系'])

# 打印DataFrame
print(df)