import pandas
import json
import os

dir = os.getcwd()
print(dir)

# Read excel document
excel_data_df = pandas.read_excel(dir + '\\Materials\\timber_grades.xlsx', sheet_name = 'Sheet1', header = 0, index_col=0)

excel_json = excel_data_df.to_json()

# Make the string into a list to be able to input in to a JSON-file
thisisjson_dict = json.loads(excel_json)

# Define file to write to and 'w' for write option -> json.dump() 
# defining the list to write from and file to write to
with open('timber_grades.json', 'w') as json_file:
    json.dump(thisisjson_dict, json_file)