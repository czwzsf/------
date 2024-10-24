import pandas as pd
import spacy  # 导入spacy库，作用是
from scipy.ndimage import label
from spacy.util import minibatch, compounding
from spacy.training.example import Example
import random
import re
import matplotlib.pyplot as plt

# Load a blank spaCy model for Chinese
nlp = spacy.blank("zh")
all_losses = []

# Create a new NER pipeline component and add it to the pipeline
ner = nlp.add_pipe("ner", last=True)  # ner的意思是命名实体识别（Named Entity Recognition）

# Read the Excel file
file_path = 'result/整车试验信息.xlsx'
df = pd.read_excel(file_path)

# Add labels to the NER component
categories = ['发动机平台', '变速箱', '桥']
for category in categories:
    ner.add_label(category)

# Prepare the training data
train_data = []

for _, row in df.iterrows():
    # Skip rows with NaN values
    configuration = str(row['配置详情']).strip() if pd.notna(row['配置详情']) else ""
    entities = []
    for category in categories:
        value = str(row[category]).strip() if pd.notna(row[category]) else ""
        # Use regular expression to find the value in the configuration
        match = re.search(re.escape(value), configuration)
        if match:
            start_idx = match.start()
            end_idx = match.end()
            entities.append((start_idx, end_idx, category))
        else:
            # Debugging: Print when a value is not found
            print(
                f'Value "{value}" for category "{category}" not found in configuration: {configuration}')
    if entities:
        train_data.append((configuration, {"entities": entities}))
    # Debugging: Print the entities for each row
    print(f'Configuration: {configuration}')
    print(f'Entities: {entities}')

# Convert to spaCy's Example objects
examples = []
for text, annotations in train_data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
    examples.append(example)

# Train the model
nlp.begin_training()
n_iter = 250

for i in range(n_iter):
    random.shuffle(examples)
    losses = {}
    # Adjust the batch size here
    batches = minibatch(examples, size=compounding(4.0, 32.0,
                                                   1.00001))
    for batch in batches:
        # drop=0.5 作用是每次训练时，随机丢弃50%的数据，防止过拟合
        nlp.update(batch, drop=0.5, losses=losses)
    all_losses.append(losses['ner'])
    print(f'Losses at iteration {i}: {losses}')

# Save the model
nlp.to_disk('model')

# Load the model and test
nlp2 = spacy.load('model')

# Test with a sample configuration detail text
test_text = '牵引,锡柴CA6SM4A51E61N,一汽CA12TAX260A(自动挡全铝壳),萨克斯Ф430,DY011前轴(盘式制动),435升级冲焊桥(带轮间差速锁/速比3.7/鼓式制动),300*80*8,JH6凸地板大排半高顶驾驶室(四点空气悬置/空调/电动举升/电动门窗/电动电加热后视镜),12R22.5-18PR(全车EA111轻量化钢圈),3800+1350,智行版,视频包2.0(10寸基本屏+四方位影像),视频记录仪,2000多功能方向盘,通风座椅,220V电源,自动大灯控制机构,板簧2/3,LNG-1350L*1个,碳钢气瓶框架,永磁同步电机80kW/130kW,锰酸锂电池(15kWh/C箱),180Ah蓄电池,带静电拖地带,进口阀,全车FAG轮端,机箱长换油,10/15/6万公里,PKC线束,限速89KM/H,国产EPB,ABS/ESC/FCW/LDWS,混合动力车,试制,375/1800,378KW,90牵引盘'
doc = nlp2(test_text)

# Extract and print the recognized entities
for ent in doc.ents:
    print(f'Label: {ent.label_}, Text: {ent.text}')

plt.plot(range(n_iter), all_losses, label='Ner Loss')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('NER Training Loss Over Iterations')
plt.legend()
plt.show()
