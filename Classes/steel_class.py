class Steel_Material:
    def __init__(self):
        self.density    = 7850      # kg/m3
        self.E          = 210000    # N/mm2 
        self.G          = 81000     # N/mm2
        self.f_y        = 355       # N/mm2                 # ASSUMING S355 STEEL FOR NOW
        self.f_u        = 490       # N/mm2                 # ASSUMING S355 STEEL FOR NOW
        self.gamma_M0   = 1.0
        self.gamma_M2   = 1.1    
        
# steel = Steel() # Sets steel as an object that we can input into other classes.  # not necessary, can just use the class directly as an argument.
