import matplotlib.pyplot as plt
import base_elements as be
import base_materials as bm

class connection():
    def __init__(self, Grade, dia):
        self.fixing = be.bolt(dia, Grade)
        self.loads = {}

    def arrange_bolts(self, n_rows, n_cols, a_1, a_2, a_3): 
        # Create grid arrangement
        self.n_bolts = n_rows * n_cols

        self.a_1 = a_1
        self.a_2 = a_2
        self.a_3 = a_3

        self.group_width = a_1 * (n_cols-1)

        bolts = {}

        xStart, yStart = 0,0
        x, y = xStart, yStart

        k = 1 # counter
        self.bolt_ids = []

        for i in range(n_rows):
            row_id = i+1
            
            for j in range(n_cols):
                self.bolt_ids.append(k)
                col_id = j+1

                bolts[str(k)] = {'x':x ,'y': y, 'row_id': row_id, 'load':{}}

                x += a_1

                k += 1
            
            x = xStart
            y -= a_2

        self.bolts = bolts

    def plot_bolts(self):
        ''' Plots bolt arrangement for review'''
        x = [self.bolts[x]['x'] for x in self.bolts]
        y = [self.bolts[x]['y'] for x in self.bolts]

        plt.plot(x,y,'o')
        plt.show()

    def apply_load(self, load_case, V_ed, duration):
        ''' Stores loadcase info to connection adn calculates ecc mom'''
        ecc = self.group_width/2 + self.a_3 + 50
        M_ecc = V_ed * ecc/1000 

        self.loads[load_case] = {'V_ed': V_ed, 'M_ed': M_ecc, 'duration': duration}

    def decompose_load(self):
        for load_case in self.loads:
            V_ed = self.loads[load_case]['V_ed']

            V_ed_i = V_ed / self.n_bolts

            for i in self.bolts:
                self.bolts[i]['load'][load_case] = {'Ved': V_ed_i}
       
if __name__ == "__main__":

    fixing_grade = '8.8'
    dia = 12

    cxxn = connection(fixing_grade, dia)

    cxxn.arrange_bolts(5 , 5, 100, 100)
    # cxxn.plot_bolts()
    cxxn.apply_load('LC 1', 100, 'Permanent')
    cxxn.apply_load('LC 2', 50, 'instantaneous')
    cxxn.decompose_load()

    pass

    