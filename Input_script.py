import Elements.base_materials as bm
import math as m 

# Inputs required to drive connection designer
# Geometry:
# Supported member
beam = {'b':280, 'd':520, 'service_class':2}

# Fin plate: 
finPl = {'t_pl':12, 'D':200, 'grade':'S355'}

# connection
cnxn = {'type':'Bolted', 'arrangement':'Grid', 'n_rows':3, 'n_cols':3, 'grade':8.8}
bolt = {'grade':'8.8', 'f_ub':800, 'd':20, 'A_bt':450}

a_1, a_2, a_3 = 100, 100, 50

# Actions:
load = {'LC':'LC1', 'V_ed':50, 'M_ed':20, 'duration':'medium'}

S355 = bm.Steel('S355')
timber = bm.Timber('GL28c')
fxng = bm.Fixing('8.8')

# -----------------------------------------#
# Material constants:
timber.calc_f_h0k(bolt['d'])
timber.calc_k_90(bolt['d'])

# Bolt constants: 
M_rRK = 0.3 * fxng.f_ub * bolt['d']**2.6

F_ax_bolt = fxng.f_ub * bolt['A_bt']

F_axRk = F_ax_bolt # To add washer/plate bearing capacity.
# -----------------------------------------#
# Place bolts 
n_bolts = cnxn['n_rows'] * cnxn['n_cols']

group_width = a_1 * (cnxn['n_cols'] - 1)
group_height = a_2 * (cnxn['n_rows'] - 1)
group_centre = (0,0)

group_inertia = 0
r_max = 0

bolts = {}
bolt_cols = {}
bolt_rows = {}

# Initialise bolt_col/bolt_row dicts
for i in range(cnxn['n_cols']):
    bolt_cols[i+1] = {'F_v':0, 'bolt_ids':[]}

for i in range(cnxn['n_rows']):
    bolt_rows[i+1] = {'F_h':0, 'bolt_ids':[]}

xStart, yStart = -group_width/2, group_height/2
x, y = xStart, yStart

k = 1 # counter
bolt_ids = []

for i in range(cnxn['n_rows']):
    row_id = i+1
    # bolt_rows[row_id] = {}
    
    for j in range(cnxn['n_cols']):

        bolt_ids.append(k)
        col_id = j+1

        bolt_rows[row_id]['bolt_ids'].append(k)
        bolt_cols[col_id]['bolt_ids'].append(k)

        # Distance of bolt from group centre / sum of squares of distances
        dx = group_centre[0] - x
        dy = group_centre[1] - y
        r = (dx**2 + dy**2)**0.5

        group_inertia += r**2

        if r > r_max:
            r_max = r

        bolts[str(k)] = {'x':x ,'y':y ,'row_id':row_id, 'col_id':col_id, 'dx':dx, 'dy':dy, 'r':r}

        x += a_1
        k += 1
    
    x = xStart
    y -= a_2
# -----------------------------------------#
# Decompose load and check local capacity at each fixing
V_ed = load['V_ed']
M_ed = load['M_ed']

V_ed_i = V_ed / n_bolts

for i in bolts:
    # Calc forces due to moment
    F_m = M_ed * 1000 * bolts[i]['r'] / group_inertia
    F_mx = F_m * bolts[i]['dy'] / r_max *-1
    F_my = F_m * bolts[i]['dx'] / r_max

    # Determine net components and resultant
    F_x = F_mx
    F_y = V_ed_i + F_my

    row_id = bolts[i]['row_id']
    col_id = bolts[i]['col_id']

    bolt_rows[row_id]['F_h'] += F_x
    bolt_cols[row_id]['F_v'] += F_y

    F_res = ((F_x)**2 + (F_y)**2)**0.5

    if F_x == 0:
        alpha = m.pi
    else:
        alpha = m.atan(F_y/F_x)

    alphaDeg = m.degrees(alpha)

    bolts[i]['F_x'] = F_x
    bolts[i]['F_y'] = F_y
    bolts[i]['F_res'] = F_res
    bolts[i]['alpha'] = alphaDeg

    f_hak = timber.calc_f_hak(alpha)

    #Capacity check:
    if f_hak > F_res:
        check = 'OK'
    else:
        check = 'NOT OK'

    print('Bolt {}: f_hak {} kN vs f_resultant {} kN -> {}'.format(i, round(f_hak,2), round(F_res,2), check))

pass


# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#

# -----------------------------------------#