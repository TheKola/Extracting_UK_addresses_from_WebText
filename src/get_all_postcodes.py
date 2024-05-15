import json
import re

companyNumberPostcodesDict = {}
json_file = 'data/database.json'

# Load the JSON data from the file
with open(json_file, 'r') as file:
    data = json.load(file)

# Specify the name of the column containing the data
column_name = 'NESTED_JSON_COLUMN_NAME'
company_number = 'company_number'

# Define the regex pattern
pattern = r'\b([A-Z][A-HJ-Y]?[0-9][A-Z0-9]? ?[0-9][A-Z]{2}|GIR ?0A{2})\b'
companyNumber = []

# Iterate through the data and scan the specified column for matches
for item in data:
    if column_name or company_number in item:
        websiteTxt = item[column_name]
        companyNumber = item[company_number]
        # Find all matching postcodes in the text
        extratedPostcodes = re.findall(pattern, websiteTxt)
        # Find the unique postcodes
        uniquePostcodes = list(set(extratedPostcodes))
        companyNumberPostcodesDict[companyNumber] = uniquePostcodes

for key, value in companyNumberPostcodesDict.items():
    print(f'{key}: {value}')