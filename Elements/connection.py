import matplotlib.pyplot as plt
import math as m 
import base_elements as be
import base_materials as bm

class connection():
    def __init__(self, Grade, dia):
        self.loads = {}
        self.fixing_grade = Grade
        self.fixing_dia = dia

    def define_edges():
        self.edges = {'A': True, 'B':False, 'C':True, 'D':True}

    def grain_dir():
        self.grain_dir = 'A' # or parallel to B 

    def arrange_bolts(self, n_rows, n_cols, a_1, a_2, a_3): 
        ''' Set coordinates of bolts'''
        # Create grid arrangement
        self.n_bolts = n_rows * n_cols

        self.a_1 = a_1
        self.a_2 = a_2
        self.a_3 = a_3

        self.group_width = a_1 * (n_cols - 1)
        self.group_height = a_2 * (n_rows - 1)
        self.group_centre = (0,0)

        self.group_inertia = 0
        self.r_max = 0

        bolts = {}

        xStart, yStart = -self.group_width/2, self.group_height/2
        x, y = xStart, yStart

        k = 1 # counter
        self.bolt_ids = []

        for i in range(n_rows):
            row_id = i+1
            
            for j in range(n_cols):
                self.bolt_ids.append(k)
                col_id = j+1

                # Distance of bolt from group centre / sum of squares of distances
                dx = self.group_centre[0] - x
                dy = self.group_centre[1] - y
                r = (dx**2 + dy**2)**0.5

                self.group_inertia += r**2

                if r > self.r_max:
                    self.r_max = r

                bolts[str(k)] = be.bolt(self.fixing_dia, self.fixing_grade, x, y, row_id, col_id, dx, dy, r)

                x += a_1
                k += 1
            
            x = xStart
            y -= a_2

        self.bolts = bolts

    def plot_bolts(self):
        ''' Plots bolt arrangement for visual review'''
        x = [self.bolts[x]['x'] for x in self.bolts]
        y = [self.bolts[x]['y'] for x in self.bolts]

        plt.plot(x,y,'o')
        plt.show()

    def apply_load(self, load_case, V_ed, M_ed, duration):
        ''' Stores loadcase info to connection adn calculates ecc mom'''
        ecc = self.group_width/2 + self.a_3 + 50
        M_ecc = V_ed * ecc/1000 

        self.loads[load_case] = {'V_ed': V_ed, 'M_ed': M_ecc + M_ed, 'duration': duration}

        print('Loadcase {} - Ved = {} kN, Med = {} kNm, Mecc = {} kNm'.format(load_case, V_ed, M_ed, M_ecc))

    def decompose_load(self):
        ''' Determine each load to each bolt'''
        n_bolts = self.n_bolts
        
        for LC in self.loads:
            V_ed = self.loads[LC]['V_ed']
            M_ed = self.loads[LC]['M_ed']

            V_ed_i = V_ed / n_bolts

            for i in self.bolts:
                # Calc forces due to moment
                F_m = M_ed * 1000 * self.bolts[i].r / self.group_inertia
                F_mx = F_m * self.bolts[i].dy / self.r_max *-1
                F_my = F_m * self.bolts[i].dx / self.r_max

                # Determine net components and resultant
                F_x = F_mx
                F_y = V_ed_i + F_my

                F_res = ((F_x)**2 + (F_y)**2)**0.5
                if F_x == 0:
                    alpha = m.pi
                else:
                    alpha = m.atan(F_y/F_x)
                
                alpha = m.degrees(alpha)

                self.bolts[i].store_decomp_ld(LC, F_x, F_y, F_res, alpha)

                # self.bolts[i]['load'][load_case].= {'F_x': F_x, 'F_y': F_y, 'F_res':F_res, 'alpha': alpha}
                # print('Bolt {} - F_x = {} kN, F_y = {} kN, F_res = {} kN, alpha = {} deg'.format(i, round(F_x), round(F_y), round(F_res), round(alpha)))

if __name__ == "__main__":

    fixing_grade = '8.8'
    timber_grade = 'GL28h'
    dia = 20

    b = 200
    d = 400

    beam_1 = be.section(b, d, timber_grade)

    cxxn = connection(fixing_grade, dia)

    cxxn.arrange_bolts(2 , 2, 100, 100, 50)
    # cxxn.plot_bolts()
    cxxn.apply_load('LC 1', 1, 50, 'Permanent')

    cxxn.decompose_load()

    beam_1.calc_f_h0k(dia)

    beam_1.calc_k_90(dia)

    beam_1.calc_f_hak(m.radians(46))

    pass

    