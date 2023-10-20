# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:20:17 2023

@author: PSCOTT
"""

import Functions.excel_report as er

def recess(cxn, fire_time):
    cxn.recess_dims()
    
    if cxn.recessed == 'Y':
        cxn.dia_recess = list[str(cxn.d)]['dia_recess']
        cxn.dp_recess  = list [str(cxn.d)]['dp_recess']
        
        if (cxn.type == 'Bolted' and cxn.bolt_hidden == 'Y') or cxn.type == 'Dowelled':
            cxn.t_plug = 10
            
            if fire_time > 0:
                min_depth = cxn.plug_fire_dim(cxn, fire_time)
                
                if cxn.t_plug < min_depth:
                    cxn.t_plug = min_depth                    
            
            # cxn.dp_recess += t_plug
            
    elif fire_time > 0:
        print('Error recessed and plug required for fire protection')
        print('Reset input')
        
# ............................................. #
def plug_fire_dim(cxn, fire_time):
        
    if fire_time > 0:
        list = {'30': 25,
                '60': 45,
                '90': 65,
                '120': 90}
        
        min_depth = list[str(int(fire_time))]
        cxn.H_p = list[str(int(fire_time))]
        
    return min_depth

# ............................................ # 
def recess_dia(cxn):
    list = {'12': {'dia_recess': 40, 'dp_recess':20},
            '16': {'dia_recess': 50, 'dp_recess': 25},
            '20': {'dia_recess': 65, 'dp_recess': 30},
            '24': {'dia_recess': 75, 'dp_recess': 35},
            '30': {'dia_recess': 95, 'dp_recess': 40}}
        
    cxn.dia_recess = list[str(cxn.d)]['dia_recess']
    cxn.dp_recess  = list [str(cxn.d)]['dp_recess']
        
# --------------------------------------------------------------------------- #        
def dowel_dims(cxn, t_char):
    list = {'12':{'dim_A': 7,  'dim_B': 4, 'h_dia_tmb': 12, 'h_dia_st': 14},
            '16':{'dim_A': 9,  'dim_B': 5, 'h_dia_tmb': 16, 'h_dia_st': 18},
            '20':{'dim_A': 9,  'dim_B': 5, 'h_dia_tmb': 20, 'h_dia_st': 22},
            '24':{'dim_A': 10, 'dim_B': 6, 'h_dia_tmb': 24, 'h_dia_st': 26},
            }
    
    cxn.dim_A      = list[str(int(cxn.d))]['dim_A']        # dimension along
    cxn.dim_B      = list[str(int(cxn.d))]['dim_B']        # dimension trans to dowel axis
    cxn.h_dia_tmb  = list[str(int(cxn.d))]['h_dia_tmb']
    cxn.h_dia_st   = list[str(int(cxn.d))]['h_dia_st']
        
    end_clr = 10    # clearance of bolt end to end of predrill
    end_wdth = 20   # min width of timber remaining next to dowel
        
    if end_wdth < t_char:
        end_wdth = t_char
    
    cxn.dowel_clr = end_clr + end_wdth + cxn.dim_A
    
# --------------------------------------------------------------------------- #
def slot_thickness(cxn):           # thickness of slot to accom. plate
    slot_list = {'10': 15,
                 '12': 20,
                 '15': 25,
                 '20': 30}
        
    cxn.slot_thk = slot_list[str(int(cxn.pl_thk))]

# --------------------------------------------------------------------------- #        
def pl_clearance(cxn,h):               # clearance from end of beam.
    if h < 1000:
        cxn.pl_clr = 10
    else:
        cxn.pl_clr = 20
        
def recess_dim(cxn):
    list = {'12': {'dia_recess': 40, 'dp_recess':20},
            '16': {'dia_recess': 50, 'dp_recess': 25},
            '20': {'dia_recess': 65, 'dp_recess': 30},
            '24': {'dia_recess': 75, 'dp_recess': 35},
            '30': {'dia_recess': 95, 'dp_recess': 40}}
    
    d = str(int(cxn.d))   
    
    cxn.D_r = list[d]['dia_recess']
    cxn.H_r  = list[d]['dp_recess']
    
    er.print_result(cxn, 'Recess diameter', cxn.D_r)
    er.print_result(cxn, 'Recess depth', cxn.H_r)

# --------------------------------------------------------------------------- #      
def determineT1(cxn,el):
    slot_thickness(cxn)
    cxn.t1 = (el.t - cxn.slot_thk) / 2
    fire_time = el.fire_time
    
    if fire_time > 0:
        t_char  = el.d_char_ef
        
        if cxn.type == 'Bolted':
            if cxn.recessed == 'Y':
                recess_dim(cxn)                
                                
                if cxn.concealed == 'Y':
                    plug_fire_dim(cxn, fire_time)
                    
                    cxn.t1 -= (cxn.H_p + cxn.H_r)

                else:
                    er.print_error(cxn, "Connection must be resessed and concealed with plug")
                    
            else:
                er.print_error(cxn, "Connection must be resessed and concealed with plug")
        
        elif cxn.type == 'Dowelled':
            plug_fire_dim(cxn, fire_time)
            dowel_dims(cxn, t_char = t_char)
            
            cxn.t1 -= cxn.dowel_clr
            
    else:
        if cxn.type == 'Bolted':
            if cxn.recessed == 'Y':
                recess_dim(cxn)
                                    
                if cxn.concealed == 'Y':
                    cxn.H_p = 10
                    cxn.t1 -= (cxn.H_p + cxn.H_r)
                    
                else:
                    cxn.t1 -= cxn.H_r     
        
        elif cxn.type == 'Dowelled':
            cxn.H_p = 10
            dowel_dims(cxn, t_char = 0)
            
            cxn.t1 -= cxn.dowel_clr
            
    er.print_result(cxn, 'Embedment, t_1',     cxn.t1)
            
# --------------------------------------------------------------------------- #    
def polarInertia(cxn):
    #Determine Inertia of bolt group
    cxn.sArray = [] #List of distance from each bolt to group center
    cxn.inertiaGroup = 0 #mm2
    
    for i in list(range(len(cxn.xCoord))):
        
        dx = cxn.xCoord[i]-cxn.groupCentreX
        dy = cxn.yCoord[i]-cxn.groupCentreY
        
        cxn.sArray.append( (dx**2 + dy**2)**0.5 )
        cxn.inertiaGroup = cxn.inertiaGroup + cxn.sArray[i]**2
        
# --------------------------------------------------------------------------- # 

# Bolt arrangement functions
# --------------------------------------------------------------------------- #
def gridArrangement(cxn):
    
    cxn.rowYcoord, cxn.colXcoord    = [], []
    cxn.rowID, cxn.colID            = [], []
    cxn.xCoord, cxn.yCoord          = [], []
    
    nextXCoord  = -cxn.a_2 * (cxn.n_para -1)/2 
    nextYCoord  = -cxn.a_1 * (cxn.n_perp -1)/2
        
    for i in list(range(cxn.n_para)):                   # Iterate second through cols
        
        for j in list(range(cxn.n_perp)):               # Iterate first through rows

            cxn.yCoord.append(nextYCoord)
            cxn.xCoord.append(nextXCoord)
            
            # Row identification
            if nextYCoord in cxn.rowYcoord:
                cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
                
            else:
                cxn.rowYcoord.append(nextYCoord)
                cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
                
            nextYCoord = cxn.yCoord[-1]+cxn.a_1
                  
            # Column identification
            if nextXCoord in cxn.colXcoord:
                cxn.colID.append(cxn.colXcoord.index(nextXCoord))
                
            else:
                cxn.colXcoord.append(nextXCoord)
                cxn.colID.append(cxn.colXcoord.index(nextXCoord))
            
        nextXCoord = cxn.xCoord[-1]+cxn.a_2    
        nextYCoord = -cxn.a_1 * (cxn.n_perp-1)/2
        
    cxn.n_bolts    = len(cxn.xCoord)
    
# --------------------------------------------------------------------------- #
def perimeterArrangement(cxn):
     
     cxn.rowYcoord, cxn.colXcoord    = [], []
     cxn.rowID, cxn.colID            = [], []
     cxn.xCoord, cxn.yCoord          = [], []
     
     nextXCoord          = -cxn.a_2 * (cxn.n_para -1)/2 
     nextYCoord          =-cxn.a_1 * (cxn.n_perp -1)/2
     
     for i in list(range(cxn.n_para)):                # Iterate second through cols
         
         for j in list(range(cxn.n_perp)):             # Iterate first through rows
             if i == 0 or i == cxn.n_para-1:
                 cxn.yCoord.append(nextYCoord)
                 cxn.xCoord.append(nextXCoord)
                 
                 # Row identification
                 if nextYCoord in cxn.rowYcoord:
                     cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
                     
                 else:
                     cxn.rowYcoord.append(nextYCoord)
                     cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
                 
                 nextYCoord = cxn.yCoord[-1]+cxn.a_1
                 
                 # Column identification
                 if nextXCoord in cxn.colXcoord:
                     cxn.colID.append(cxn.colXcoord.index(nextXCoord))
                     
                 else:
                     cxn.colXcoord.append(nextXCoord)
                     cxn.colID.append(cxn.colXcoord.index(nextXCoord))
                 
             elif j == 0 or j == cxn.n_perp-1:   
                 cxn.yCoord.append(nextYCoord)
                 cxn.xCoord.append(nextXCoord)       
                 
                 # Row identification
                 if nextYCoord in cxn.rowYcoord:
                     cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
                     
                 else:
                     cxn.rowYcoord.append(nextYCoord)
                     cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
                 
                 nextYCoord = cxn.yCoord[-1]+cxn.a_1*(cxn.n_perp-1)
                   
                 # Column identification
                 if nextXCoord in cxn.colXcoord:
                     cxn.colID.append(cxn.colXcoord.index(nextXCoord))
                     
                 else:
                     cxn.colXcoord.append(nextXCoord)
                     cxn.colID.append(cxn.colXcoord.index(nextXCoord))
             
         nextXCoord = cxn.xCoord[-1]+cxn.a_2   
         nextYCoord = -cxn.a_1*(cxn.n_perp-1)/2  
         
     cxn.n_bolts    = len(cxn.xCoord)

# --------------------------------------------------------------------------- #   
def circularArrangement(cxn):
    import math as m
    
    cxn.rowYcoord, cxn.colXcoord    = [], []
    cxn.rowID, cxn.colID            = [], []
    cxn.xCoord, cxn.yCoord          = [], []
    
    radius = cxn.radius
            
    cxn.xCoord.append(0)
    cxn.yCoord.append(radius)                          # First bolt specified
    
    cxn.rowID.append(0) 
    cxn.colID.append(0)                                # First bolt row/col specified
    
    cxn.colXcoord.append(0) 
    cxn.rowYcoord.append(radius)                       # First bolt row/col is first bolt coords
        
    chordAngle = 2*m.pi / cxn.n_bolts            # Find angle between bolts
    angle = chordAngle                                  # Angle to second bolt
    
    for i in range(cxn.n_bolts-1):
        nextXCoord = round(radius * m.sin(angle),2)
        nextYCoord = round(radius * m.cos(angle),2)
           
        cxn.xCoord.append(nextXCoord)
        cxn.yCoord.append(nextYCoord)
           
        angle = angle + chordAngle
           
        # Row identification
        if nextYCoord in cxn.rowYcoord:
            cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
                
        else:
            cxn.rowYcoord.append(nextYCoord)
            cxn.rowID.append(cxn.rowYcoord.index(nextYCoord))
              
            # Column identification
        if nextXCoord in cxn.colXcoord:
            cxn.colID.append(cxn.colXcoord.index(nextXCoord))
           
        else:
            cxn.colXcoord.append(nextXCoord)
            cxn.colID.append(cxn.colXcoord.index(nextXCoord))
        
# --------------------------------------------------------------------------- #   
def boltGroupProperties(cxn):
# Determines geometric properties of bolt group and reports to s/sheet     
    cxn.groupCentreX, cxn.groupCentreY = 0, 0
                
    if cxn.arrangement == "Grid":
        gridArrangement(cxn)
            
    elif cxn.arrangement == "Perimeter":
        perimeterArrangement(cxn)
    
    elif cxn.arrangement == "Circular":                                         # missing circular arrangement option
        pass 

    cxn.polarInertia = polarInertia(cxn)
        
# --------------------------------------------------------------------------- # 