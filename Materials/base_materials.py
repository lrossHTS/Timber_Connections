class Timber:
    def __init__(self,Grade):
        self.f_vk = 3.5 # MPa
        self.f_c90k = 2.5 # MPa
        self.f_c0k = 28 # MPa
        self.rho_k = 425 # kg/m3
        
        self.gamma_m = 1.25

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

    my_beam = Timber('GL28')
    your_beam = Timber('GL24')
    steel_test = Steel('S355')
    fixing_test = Fixing('8.8')

pass               
                    