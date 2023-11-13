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
        self.f_h0k = 0.082 * (1 - 0.01*dia) * self.rho_k # MPa

    def calc_k_90(self, dia):
        ''' Calcs k90 - eq 8.33'''
        f_types = {'softwood':1.35, 'LVL': 1.3, 'hardwood': 0.9}

        # add condition to pick type
        f = f_types['softwood']

        self.k_90 = f + 0.015 * dia

    def calc_f_hak(self, alpha):
        ''' Calcs char embed str at angle to grain - eq 8.31'''
        return self.f_h0k / (self.k_90*m.sin(alpha)**2 + m.cos(alpha)**2) # MPa
        
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
    def __init__(self, dia, Grade):
        self.Grade = Grade

        properties = load_data('fixing_grades')[Grade]
        for key, value in properties.items():
            setattr(self, key, value)

        self.d = dia
    
    @property
    def calc_M_yRk(self):
        self.M_yRk = 0.3 * self.f_ub * self.d**2.6 # Nmm

    @property
    def calc_F_axRk(self):
        self.F_axRk = 35.1 * 1000 # N

    def calc_n_ef(self, a_1, n):
        n_ef = min(n, n**0.9 * (a_1 / (13*self.d))**0.25)
        return n_ef

    def calc_F_vRK_dble_shear(self, t_1, f_hak):
        # EN1995-1-1 Equation 8.11
        f = f_hak * t_1 * self.d
        g = f_hak * t_1 * self.d * ((2 + 4*self.M_yRk / (f_hak*self.d*t_1**2))**0.5 - 1) + self.F_axRk/4
        h = 2.3 * (self.M_yRk * f_hak * self.d)**0.5 + self.F_axRk / 4

        F_vRk = min(f,g,h)

        return F_vRk / 1000 # convert to kN

    def calc_F_vRd(self, F_vRk, k_mod):
        return k_mod * F_vRk / self.gamma_m2

# Test run
if __name__ == "__main__":

    beam_test = Timber('GL28c')
    steel_test = Steel('S355')
    fixing_test = Fixing('8.8')

pass             