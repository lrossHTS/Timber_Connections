import pandas
import json
from os import path

def load_excel(file_name):
    base_dir = path.dirname(path.dirname(__file__))
    file_path = path.join(base_dir, "data", file_name + ".xlsx")
    if path.isfile(file_path):
        excel = pandas.read_excel(file_path, sheet_name = 'Sheet1', header = 0, index_col=0)
    
    excel_json = excel.to_json()

    # Make the string into a list to be able to input in to a JSON-file
    excel_json_list = json.loads(excel_json)

    json_file = path.join(base_dir, "data", file_name + ".json") 

    # Define file to write to and 'w' for write option -> json.dump() 
    # Defining the list to write from and file to write to
    with open(json_file, 'w') as json_file:
        json.dump(excel_json_list, json_file)

data_files = ['timber_grades', 'steel_grades', 'fixing_grades']

for file_name in data_files:
    load_excel(file_name)