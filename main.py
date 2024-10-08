import os
import pandas as pd
from docx import Document
# 文件地址
path = "data/Data_JH6"
# 获取文件夹下所有文件
files = [f for f in os.listdir(path) if f.endswith('.docx')]
# 创建一个DataFrame
data_name = pd.DataFrame(files, columns=["filename"])

# 新建一个空的DataFrame，用来存储每一个docx中的需要清洗的数据
data_result = pd.DataFrame()

# 读取每一个docx文件
for file in files:
    # 读取docx文件
    doc = Document(path + '/' + file)
    # 打印内容
    for para in doc.paragraphs:
        print(para.text)

