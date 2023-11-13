import Elements.base_materials as bm
import math as m 

# Inputs required to drive connection designer
# Geometry:
# Supported member
beam = {'b':280, 'd':520, 'service_class':2}

# Fin plate: 
finPl = {'t_pl':12, 'D':200, 'grade':'S355'}

t_1 = (beam['b'] - finPl['t_pl']) / 2

# connection
cnxn = {'type':'Bolted', 'arrangement':'Grid', 'n_rows':2, 'n_cols':2, 'grade':8.8}

a_1, a_2, a_3 = 100, 100, 50

# Actions:
load = {'LC':'LC1', 'V_ed':10, 'M_ed':10, 'duration':'medium'}

k_mod = 0.8

S355 = bm.Steel('S355')
timber = bm.Timber('GL28c')
bolt = bm.Fixing(20, '8.8')

# -----------------------------------------#
# Material constants:
timber.calc_f_h0k(bolt.d)
timber.calc_k_90(bolt.d)

# Bolt constants: 
bolt.calc_M_yRk
bolt.calc_F_axRk

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
V_ed = load['V_ed'] / 2 # as in double shear
M_ed = load['M_ed'] / 2 # as in double shear

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

    F_vRk = bolt.calc_F_vRK_dble_shear(t_1, f_hak)
    F_vRd = bolt.calc_F_vRd(F_vRk, k_mod)

    #Capacity check:
    if F_vRd > F_res:
        check = 'OK'
    else:
        check = 'NOT OK'

    print('Bolt {}: F_vRd {} kN vs F_resultant {} kN -> {}'.format(i, round(F_vRd,1), round(F_res,1), check))

print('')

# -----------------------------------------#
# Check bolt row capacity
# F_vRd parallel to grain
f_hak_para = timber.calc_f_hak(0)
F_vRk_para = bolt.calc_F_vRK_dble_shear(t_1, f_hak)
F_vRd_para = bolt.calc_F_vRd(F_vRk, k_mod)

for i in bolt_rows:
    n = len(bolt_rows[i]['bolt_ids'])
    n_eff = bolt.calc_n_ef(a_1, n)

    F_vRd_row = n_eff * F_vRd_para
    F_vEd_row = abs(bolt_rows[i]['F_h'])

    if F_vRd_row > F_vEd_row:
        check = 'OK'
    else:
        check = 'NOT OK'

    print('Row {}: F_vRd of row: {} kN vs F_resultant {} kN -> {}'.format(i, round(F_vRd_row,1), round(F_vEd_row,1), check))
# -----------------------------------------#
pass