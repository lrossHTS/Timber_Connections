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
    def __init__(self, dia, Grade):
        super()__init__(Grade)

        self.dia = dia

class dowel(bm.Fixing):
    def __init__(self, dia, Grade):
        super()__init__(Grade)

        self.dia = dia

# Test run
if __name__ == "__main__":

    Grade = 'GL28c'
    span = 3000 
    b = 200
    d = 400

    beam = beam(span, Grade, b, d)

    pass

