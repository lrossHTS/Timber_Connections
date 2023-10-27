# Inputs required to drive connection designer

# Geometry:
# Supported member
b = 280 # mm
d = 520 # mm

# Supporting member:
b = 300 # mm
d = 300 # mm

# Fin plate: 
t_pl = 12 # mm
d_pl = 200 # mm

# Fixing:
type = 'Bolted' # or 'Dowelled'
dia = 20 # mm
arrangement = 'Grid' # or 'Perimeter'
n_bolt_rows = 3
n_bolt_columns = 3

# Actions:
beam_shear = 30 # kN
# beam_axial 
# beam bending 

# Material Grades:
bolts = '8.8'
plate = '355'
timber = 'GL28h'

# Environment
service_class = 2 # or 1 or 3

# Loading properties:
load_duration = 'medium'

# Timber specific properties / factors (Grade)
f_vk = 3.5 # MPa
f_c90k = 2.5 # MPa
f_c0k = 28 # MPa
rho_k = 425 # kg/m3

gamma_m = 1.25

# Bolt specific properties / factors (Grade)
f_yb = 640 # MPa
f_ub = 800 # MPa

gamma_m2 = 1.25

# Fin plate specific properties / factors (Grade)
f_yp = 355 # MPa
f_up = 490 # MPa

gamma_m0 = 1.0
gamma_pl_m2 = 1.25


