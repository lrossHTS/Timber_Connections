import json
import os
import sys
from os import path
from pprint import pprint

dir = os.getcwd()
# pprint(sys.path)

# data_dir = dir + '\\Data'
# sys.path.append(data_dir)

file_name = 'timber_grades'

def load_data(file_name):
    base_dir = path.dirname(path.dirname(__file__))
    file_path = path.join(base_dir, "data", file_name + ".json")
    if path.isfile(file_path):
        with open(file_path, 'r') as fh:
            return json.load(fh)


class Timber:
    def __init__(self,Grade):
        # Import timber_grade_json
        # Open JSON
        # f = open("timber_grades.json")

        properties = load_data('timber_grades')[Grade]
        for key, value in properties.items():
            setattr(self, key, value)

        test = 1

class Steel:
    def __init__(self, Grade):
        self.f_yp = 355 # MPa
        self.f_up = 490 # MPa

        self.gamma_m0 = 1.0
        self.gamma_m2 = 1.25

class Fixing:
    def __init__(self, Grade):
        self.f_yb = 640 # MPa
        self.f_ub = 800 # MPa

        self.gamma_m2 = 1.25

if __name__ == "__main__":

    dir = os.getcwd()
    my_beam = Timber('GL28c')
    your_beam = Timber('GL24')
    steel_test = Steel('S355')
    fixing_test = Fixing('8.8')

pass               
                    