import math as m

# --------------------------------------------------------------#    
def dist_reqmts(cxn):
    v_1 = cxn.v_1_cxn
    v_2 = cxn.v_2_cxn
    d   = cxn.d
    
    fixing_type = cxn.type
    
    try:
        alpha = m.atan(v_2 / v_1 )
    except:
        alpha = 0
        
    dist_reqmts = {}
    
    if fixing_type == 'Bolted': 
        # Spacing parallel to grain (a_1)
        a_1 = d * (4 + abs(m.cos(alpha)))
        
        # ---------------------------------------------- #
        # Perp to grain (a_2)
        a_2 = 4 * d
        
        dist_reqmts['a_1'] = a_1
        dist_reqmts['a_2'] = a_2
        
        # ---------------------------------------------- #
        # End distance:
        # Check if force is towards/away from beam end
        
        if v_1 < 0: # if neg, v_1 is towards beam end
            a_3t = max (7*d, 80)
            
            dist_reqmts['a_3t'] = a_3t
            dist_reqmts['a_3c'] = 0
        
        else: # v_1 is away from beam end -> check angle rel. to grain
            
            if alpha < m.radians(30):  # note that 30 deg is 0.524 rad
                a_3c = 4 * d
            
            else:
                a_3c = (1 + 6 * abs(m.sin(alpha))) * d
            
            dist_reqmts['a_3c'] = a_3c
            dist_reqmts['a_3t'] = 0
        
        # ---------------------------------------------- #
        # Edge distance: 
        #   Calc a_4t & a_3t (minimum required)
        a_4t = max ((2 + 2*m.sin(alpha))*d, 3 * d)
        a_4c = 3 * d
                  
        dist_reqmts['a_4t'] = a_4t
        dist_reqmts['a_4c'] = a_4c

    elif fixing_type == 'Dowelled':
        # Spacing parallel to grain (a_1)
        a_1 = (3 + 2* m.cos(alpha)) * d    
        
        # Perp to grain (a_2)
        a_2 = 3 * d  
        
        dist_reqmts['a_1'] = a_1
        dist_reqmts['a_2'] = a_2
    
        # ---------------------------------------------- #    
        # End distance:
        # Check if force is towards/away from beam end
    
        a_3t = max (7*d, 80)
        
        if v_1 < 0: # if neg, v_1 is towards beam end
            
            dist_reqmts['a_3t'] = a_3t
            dist_reqmts['a_3c'] = 0
        
        else: # v_1 is away from beam end -> check angle rel. to grain
            
            if alpha < m.radians(30):                 # note that 30 deg is 0.524 rad
                a_3c = max(3.5 * d, 40)
            
            else:
                a_3c = a_3t * abs(m.sin(alpha))
            
            dist_reqmts['a_3c'] = a_3c
            dist_reqmts['a_3t'] = 0
        
        # ---------------------------------------------- #
        # Edge distance: 
        #   Calc a_4t & a_3t (minimum required)
        a_4t = max ((2 + 2*m.sin(alpha))*d, 3 * d)
        a_4c = 3 * d
        
        dist_reqmts['a_4t'] = a_4t
        dist_reqmts['a_4c'] = a_4c
        
    else: 
        print('Connection type not supported')
             
    return dist_reqmts

# -------------------------------------------------------------------------- #       
def meas_dists(cxn,h):
    cxn.dists = []
    
    for i in range(len(cxn.xCoord)):
        d = {}
        
        d['a_1'] = cxn.a_1
        d['a_2'] = cxn.a_2
        
        #a_3t
        # print(cxn.v_1[i])
        # print(cxn.a_3_group)
        if cxn.v_1[i] < 0: # if less than 0, force towards element end

            d['a_3t'] = cxn.a_3_group + max(cxn.yCoord) - cxn.yCoord[i]
            # print(d['a_3t'] )
        
        #a_3c
        else: # otherwise, force is away from end
            d['a_3c'] = cxn.a_3_group + max(cxn.yCoord) - cxn.yCoord[i]
            # print(d['a_3c'] )
            
        #a_4
        a_4pos = h/2 - cxn.xCoord[i] # bolt distance to positive edge
        a_4neg = h   - cxn.xCoord[i] # bolt distance to negative edge
        
        #a_4c
        if cxn.xCoord[i] >= 0: # Bolt is closer to positive edge (Check which side of beam that bolt is on)

            if cxn.v_2[i] >= 0: # positive -> towards edge
                d['a_4t']   = a_4pos
                d['a_4c']   = a_4neg
          
            else: # v_2 is positive -> towards edge
                d['a_4t']   = a_4neg
                d['a_4c']   = a_4pos
          
        else: # Bolt is closer to negative edge

            if cxn.v_2[i] <= 0: # v_2 is negative -> towards edge
                d['a_4t']   = a_4neg
                d['a_4c']   = a_4pos
            else:
                d['a_4t']   = a_4pos
                d['a_4c']   = a_4neg   
                
        cxn.dists.append(d)
        
 # -------------------------------------------------------------------------- #   
def checkEdgeDistances(cxn, h):
          
    cxn.geometryStatus = "OK"
    meas_dists(cxn,h)
    
    cxn.reqs = []
    
    for i in range(len(cxn.xCoord)): 
        cxn.reqs.append( dist_reqmts(cxn) )                   
                
    # Check spacing parallel to grain (vert spacing)
        if cxn.dists[i]['a_1'] < cxn.reqs[i]['a_1']:
            print("Vertical spacing less than minimum!")
            print('at bolt', i + 1)
            print('Spacing provided = ', cxn.dists[i]['a_1'], ' mm')
            print('Minimum spacing = ', cxn.reqs[i]['a_1'], ' mm')
            print()
            
            cxn.geometryStatus = "NOT OK"
                
    # Check spacing perpindicular to grain (horiz spacing)
        if cxn.dists[i]['a_2'] < cxn.reqs[i]['a_2']:
            print('Horizontal spacing less than minimum!')
            print('at bolt', i + 1)
            print('Spacing provided = ', cxn.a_2, ' mm')
            print('Minimum spacing = ', cxn.reqs[i]['a_2'], ' mm')
            print()
            
            cxn.geometryStatus = "NOT OK"
    
    # Check distance to beam end
        if cxn.v_1[i] < 0 and cxn.dists[i]['a_3t'] < cxn.reqs[i]['a_3t']:
            print('Distance to loaded beam end less than minimum!')
            print('at bolt', i + 1)
            print('Distance provided = ', cxn.dists[i]['a_3t'] , ' mm')
            print('Minimum distance = ', cxn.reqs[i]['a_3t'], ' mm')
            print()
            
            cxn.geometryStatus = "NOT OK"
            
        elif cxn.v_1[i] > 1 and cxn.dists[i]['a_3c'] < cxn.reqs[i]['a_3c']:
            print('Distance to unloaded beam end less than minimum!')
            print('at bolt', i + 1)
            print('Distance provided = ', cxn.dists[i]['a_3c'] , ' mm')
            print('Minimum distance = ', cxn.reqs[i]['a_3c'], ' mm')
            print()
            
            cxn.geometryStatus = "NOT OK"
        
    # Check distance to beam edge
        if cxn.dists[i]['a_4t'] < cxn.reqs[i]['a_4t']:
            print('Distance to loaded beam edge less than minimum!')
            print('at bolt', i + 1)
            print('Distance provided = ', cxn.dists[i]['a_4c'] , ' mm')
            print('Minimum distance = ', cxn.reqs[i]['a_4c'], ' mm')
            print()
            
            cxn.geometryStatus = "NOT OK"
            
        if cxn.dists[i]['a_4c'] < cxn.reqs[i]['a_4c']:
            print('Distance to unloaded beam edge less than minimum!')
            print('at bolt', i + 1)
            print('Distance provided = ', cxn.dists[i]['a_4c'] , ' mm')
            print('Minimum distance = ', cxn.reqs[i]['a_4c'], ' mm')
            print()
            
            cxn.geometryStatus = "NOT OK"
         
# -------------------------------------------------------------------------- #   



