class Fixing:
    def __init__(self,type,dia,grade):

        self.type = type
        self.dia = dia
        self.grade = grade

        self.get_fixing_strength()

        self.get_k90(timber_grade) 

        if type == 'Bolt':
            self.get_net_bolt_tens_A()
        
    def get_fixing_strength(self):
        grade = self.grade
            
        boltStrengthList = {'4.6': {'f_yk': 240, 'f_uk':400},
                            '4.8': {'f_yk': 240, 'f_uk':400},
                            '5.6': {'f_yk': 240, 'f_uk':400},
                            '6.8': {'f_yk': 240, 'f_uk':400},
                            '8.8': {'f_yk': 240, 'f_uk':400},
                            '10.9':{'f_yk': 240, 'f_uk':400}}
        
        self.f_uk = boltStrengthList[grade]['f_uk']
        self.f_yk = boltStrengthList[grade]['f_yk']

    def get_net_bolt_tens_A(self):
        boltDiaList = [   5,    6,    7,    8, 10, 12,    14,  16,  18,  20,  22,  24,  27,  30]
        netAreaList = [14.2, 20.1, 28.9, 36.6, 58, 84.3, 115, 157, 192, 245, 303, 353, 459, 561]
        
        d = cxn.d
        
        if d in boltDiaList:
            cxn.A_boltNet = netAreaList[boltDiaList.index(d)]   
        else:
            print('Bolt diameter not supported')

    def get_k90(self, timber_grade):
        
        if timber_grade in ["C16", "C24", "C27", "GL24c", "GL28c", "GL32c", "GL24h", "GL28h", "GL32h", "GL75"]:
            self.k_90 = 1.35 + 0.015 * self.dia
        else:
            print("Grade not supported")
            self.k_90 = None 