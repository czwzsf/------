import pandas as pd
import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example

# Load the spaCy model
nlp = spacy.blank('zh')

# Add the text categorizer to the pipeline
if 'textcat_multilabel' not in nlp.pipe_names:
    textcat = nlp.add_pipe('textcat_multilabel', last=True)
else:
    textcat = nlp.get_pipe('textcat_multilabel')

# Add labels to the text categorizer
textcat.add_label('ENGINE')
textcat.add_label('TRANSMISSION')
textcat.add_label('AXLE')

# Read the Excel file
file_path = 'result/整车试验信息.xlsx'
df = pd.read_excel(file_path)

# Prepare the data
df['target'] = df[['发动机平台', '变速箱', '桥']].apply(lambda x: ' '.join(map(str, x)), axis=1)
train_data = [(str(row['配置详情']), {'cats': {'ENGINE': 1 if row['发动机平台'] else 0,
                                               'TRANSMISSION': 1 if row['变速箱'] else 0,
                                               'AXLE': 1 if row['桥'] else 0}}) for _, row in df.iterrows()]

# Train the model
n_iter = 10
optimizer = nlp.begin_training()

for i in range(n_iter):
    losses = {}
    batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
        examples = [Example.from_dict(nlp.make_doc(text), annotation) for text, annotation in zip(texts, annotations)]
        nlp.update(examples, drop=0.5, losses=losses)
    print(f'Losses at iteration {i}: {losses}')

# Save the model
nlp.to_disk('model')

# Load the model and test
nlp2 = spacy.load('model')
doc = nlp2('Your configuration details here')
print(doc.cats)

# Load the trained model
nlp2 = spacy.load('model')

# Test with a sample configuration detail text
test_text = '牵引,潍柴WP13NG540E60,陕齿F12JZ26A(自动挡全铝壳)+液力缓速器,EATONФ430,DY011前轴(盘式制动),435升级冲焊桥(带轮间差速锁/速比3.417/鼓式制动),300*80*8,JH6凸地板大排半高顶驾驶室(四点空气悬置/空调/电动举升/电动门窗/电动电加热后视镜),12R22.5-18PR(全车EA111轻量化钢圈),3800+1350,TS,智行版,北方款(独立暖风+电加热座椅),视频包2.0(10寸基本屏+四方位影像),内外饰色彩优化,视频记录仪,2000多功能方向盘,通风座椅,220V电源,自动大灯控制机构,板簧2/2,LNG-1350L*1个,DQ-2,碳钢气瓶框架,220Ah蓄电池,带静电拖地带,进口阀,全车FAG轮端,变速箱长换油,6/20/6万公里,限速89KM/H,ABS/ESC/FCW/LDWS,试制,392/1900,397KW,90牵引盘'
doc = nlp2(test_text)

# Print the predicted categories
print(doc.cats)
