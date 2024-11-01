import spacy
import os
import re
import pandas as pd
from docx import Document

# File path
path = 'data/Data_2024_10'

# Initialize an empty list to store file information
data = []

# Define known car models
known_models = ['JH6', 'JH5', '悍V', '龙V', '鹰途']

# Iterate through all files in the folder
for filename in os.listdir(path):
    if filename.endswith('.docx'):
        # Use regex to split the filename, considering different types of dashes
        parts = re.split(r'[-–—]', filename)
        if len(parts) >= 6:
            # Get car model and series
            car_model = parts[4]
            vehicle_model = None
            series = None
            # Check if the car model field contains known models
            for model in known_models:
                if model in car_model:
                    vehicle_model = model
                    series = car_model.split(model, 1)[1]
                    break
            # Read the content of the Word file
            doc = Document(os.path.join(path, filename))
            scheme_number = None
            vin_code = None
            config_details = None
            for table in doc.tables:
                for row in table.rows:
                    for i, cell in enumerate(row.cells):
                        if '方案号' in cell.text and i + 1 < len(row.cells):
                            scheme_number = row.cells[i + 1].text.strip()
                        if 'VIN码' in cell.text and i + 1 < len(row.cells):
                            vin_code = row.cells[i + 1].text.strip()[-8:]
                        if '样车配置' in cell.text and i + 1 < len(row.cells):
                            config_details = row.cells[i + 1].text.strip()
                        if '项目名称' in cell.text and i + 1 < len(row.cells):
                            project_name = row.cells[i + 1].text.strip()
                        if '试验理由' in cell.text and i + 1 < len(row.cells):
                            test_reason = row.cells[i + 1].text.strip()
                        if '试验方案' in cell.text and i + 1 < len(row.cells):
                            test_plan = row.cells[i + 1].text.strip()
                        if '试验时间' in cell.text and i + 1 < len(row.cells):
                            test_time = row.cells[i + 1].text.strip()
            # Add the information to the list
            if vehicle_model and series and scheme_number and vin_code and config_details:
                data.append([vehicle_model, series, scheme_number,
                            vin_code, config_details, project_name, test_reason, test_plan, test_time])

# Convert the list to a DataFrame
df = pd.DataFrame(
    data, columns=['车型', '品系', '方案号', 'VIN码', '样车配置', '项目名称', '试验理由', '试验方案', '试验时间'])

# # Load the trained model
# nlp = spacy.load('model')


# # Function to extract engine and gearbox information
# def extract_info(text):
#     doc = nlp(text)
#     engine = None
#     gearbox = None
#     bridge = None
#     for ent in doc.ents:
#         if ent.label_ == '发动机平台':
#             engine = ent.text
#         elif ent.label_ == '变速箱':
#             gearbox = ent.text
#         elif ent.label_ == '桥':
#             bridge = ent.text

#     return engine, gearbox, bridge


# # Apply the function to each row in the DataFrame
# df[['发动机', '变速箱', '桥']] = df['样车配置'].apply(
#     lambda x: pd.Series(extract_info(x)))

# Write the updated DataFrame to an Excel file
df.to_excel('output_with_engine_gearbox.xlsx', index=False)
