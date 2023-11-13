import json
import math as m
from os import path

def load_data(file_name):
    base_dir = path.dirname(path.dirname(__file__))
    file_path = path.join(base_dir, "data", file_name + ".json")
    if path.isfile(file_path):
        with open(file_path, 'r') as fh:
            return json.load(fh)

class Timber:
    def __init__(self,Grade):
        self.Grade = Grade
        properties = load_data('timber_grades')[Grade]
        for key, value in properties.items():
            setattr(self, key, value)

    def calc_f_h0k(self, dia):
        ''' Calcs char embed str - eq 8.32'''
        self.f_h0k = 0.082*(1 - 0.01*dia) * self.rho_k

    def calc_k_90(self, dia):
        ''' Calcs k90 - eq 8.33'''
        f_types = {'softwood':1.35, 'LVL': 1.3, 'hardwood': 0.9}

        # add condition to pick type
        f = f_types['softwood']

        self.k_90 = f + 0.015 * dia

    def calc_f_hak(self, alpha):
        ''' Calcs char embed str at angle to grain - eq 8.31'''
        return self.f_h0k / (self.k_90*m.sin(alpha)**2 + m.cos(alpha)**2)
        
class Steel:
    def __init__(self, Grade):
        self.Grade = Grade
        properties = load_data('steel_grades')[Grade]
        for key, value in properties.items():
            setattr(self, key, value)

        self.f_yp = 355 # MPa
        self.f_up = 490 # MPa

        self.gamma_m0 = 1.0
        self.gamma_m2 = 1.25

class Fixing:
    def __init__(self, Grade):
        self.Grade = Grade
        properties = load_data('fixing_grades')[Grade]
        for key, value in properties.items():
            setattr(self, key, value)

# Test run
if __name__ == "__main__":

    beam_test = Timber('GL28c')
    steel_test = Steel('S355')
    fixing_test = Fixing('8.8')

pass             