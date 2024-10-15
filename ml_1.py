import pandas as pd
import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example
import random
import re

# Load a blank spaCy model for Chinese
nlp = spacy.blank("zh")

# Create a new NER pipeline component and add it to the pipeline
ner = nlp.add_pipe("ner", last=True)

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
            print(f'Value "{value}" for category "{category}" not found in configuration: {configuration}')
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
n_iter = 100

for i in range(n_iter):
    random.shuffle(examples)
    losses = {}
    batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        nlp.update(batch, drop=0.5, losses=losses)
    print(f'Losses at iteration {i}: {losses}')

# Save the model
nlp.to_disk('model')

# Load the model and test
nlp2 = spacy.load('model')

# Test with a sample configuration detail text
test_text = '整车，潍柴WP14T610E62发动机（12万公里长换油），A+D悬置，120A发电机，电控硅油高置风扇，平行流中冷器，Ф430法雷奥离合器，陕齿F16JZ28A变速箱（铝壳，AMT），液力缓速器，DY020前轴（FAG免维护轮端），蓬翔440桥（速比2.687，FAG免维护轮端，轮间差速锁），前盘后鼓，12R22.5 18PR轮胎，前铝合金、后轻量化钢圈，国际优秀品牌轮胎，车架宽前940mm后800mm，纵梁断面280*80*9mm，轴距（3450+1350）mm，725L+300L铝油箱，带水加热，带水寒宝,100L尿素箱（集成），BOSCH-ECO转向机，ABS+ESC+LDWS+FCW（KNORR)，制动压力12.5bar，VOSS接头，前桥带横向稳定杆，前1880单片簧，后两片簧，V杆螺栓采用鹰途方案，立式电瓶框，220Ah蓄电池，JH6平地板大排半高顶驾驶室（后悬置后移），电动天窗，行车空调，电动加热一体式后视镜，电动门窗，带导流罩及侧翼板，格拉默座椅，驾驶室四点气囊悬置，220V电源，1KW逆变器，2000多功能方向盘（真皮包裹），旋钮开关+组合开关，PKC线束，青汽4G车联网，手电一体液压举升装置，视频包（10寸屏+四方位），家居包2.0，彩色液晶仪表，内外饰色彩优化，LED大灯，转向辅助照明，LED昼行灯，LED示廓灯，国六标贴，国六在线检测终端，智尊版，基本款，约斯特90#牵引盘。机箱桥长换油，12/20/10万公里，限速89km/h。'

doc = nlp2(test_text)

# Extract and print the recognized entities
for ent in doc.ents:
    print(f'Label: {ent.label_}, Text: {ent.text}')
