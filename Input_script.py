# Inputs required to drive connection designer

# Geometry
# Supported member
b = 280 # mm
d = 520 # mm

# Supporting member
b = 300 # mm
d = 300 # mm

# Fin plate 
t_pl = 12 # mm
d_pl = 200 # mm

# Fixing
type = 'Bolted' # or 'Dowelled'
dia = 20 # mm
arrangement = 'Grid' # or 'Perimeter'
n_bolt_rows = 3
n_bolt_columns = 3

# Actions
beam_shear = 30 # kN
# beam_axial
# beam bending 

# Material properties
bolts = '8.8'
plate = '355'
timber = 'GL28h'

# Loading properties
Duration = 'medium'
