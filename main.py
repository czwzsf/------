import os
import re
import pandas as pd
from docx import Document

# File path
path = 'data/Data_JH6'

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
            # Add the information to the list
            if vehicle_model and series and scheme_number and vin_code and config_details:
                data.append([vehicle_model, series, scheme_number, vin_code, config_details])

# Convert the list to a DataFrame
df = pd.DataFrame(data, columns=['车型', '品系', '方案号', 'VIN码', '样车配置'])

# Write the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)
