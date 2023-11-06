import base_materials as bm

class section(bm.Timber):
    def __init__(self, b, d, Grade):
        super().__init__(Grade)

        self.b = b
        self.d = d

class beam(section):
    def __init__(self, span, Grade, b, d):
        super().__init__(b, d, Grade)

        self.span = span

class column(section):
    def __init__(self, height, Grade, b, d):
        super().__init__(b, d, Grade)

        self.height = height

class fin_plate(bm.Steel):
    def __init__(self, t_pl, height, Grade):
        super().__init__(Grade)

        self.t_pl = t_pl
        self.height = height

class bolt(bm.Fixing):
    def __init__(self, dia, Grade, x, y, row_id, col_id, dx, dy, r):
        super().__init__(Grade)

        self.dia = dia    
        self.x = x
        self.y = y
        self.row_id = row_id
        self.col_id = col_id 
        self.dx = dx 
        self.dy = dy
        self.r = r
        self.loads = {}

    @property
    def M_yrk(self):
        return 0.3 * self.f_ub * self.dia**2.6
    
    def store_decomp_ld(self, LC, F_x, F_y, F_res, alpha):
        self.loads[LC]={
            'F_x' : F_x,
            'F_y' : F_y,
            'F_res' : F_res,
            'alpha' : alpha}


class dowel(bm.Fixing):
    def __init__(self, dia, Grade):
        super().__init__(Grade)

        self.dia = dia

# Test run
if __name__ == "__main__":

    Grade = 'GL28c'
    span = 3000 
    b = 200
    d = 400
    bolt_dia = 20
    bolt_grade = '8.8'

    bolt_1 = bolt(bolt_dia, bolt_grade)
    print(bolt_1.M_yrk)

    pass


