import os
import pandas as pd

path = 'data/Data_2024_10'
df = pd.DataFrame(columns=['车型', '品系', '方案号', 'VIN码', '样车配置', '文件名称'])
for filename in os.listdir(path):
    if filename.endswith('.docx'):
        #  将文件名称填入到DataFrame中
        df.loc[len(df)] = [None, None, None, None, None, filename]
df.to_excel('试验数据处理.xlsx', index=False)
