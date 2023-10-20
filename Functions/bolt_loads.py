# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:51:58 2023

@author: PSCOTT
"""

import numpy as np
import math as m
import Functions.plot_tools as pt

# --------------------------------------------------------------------------- #      
def boltLoads(cxn, el):
    inp         = cxn.input_sheet
    v_1_cxn = cxn.v_1_cxn
    v_2_cxn = cxn.v_2_cxn
    
    v_1_dir     = []
    v_2_dir     = []
    v_1_M       = []
    v_2_M       = []
    v_1         = []
    v_2         = []
    v_res       = []
    alpha       = []
    
    if max(cxn.xCoord) > el.h / 2:
        
        inp.range('G14').font.bold      = True
        inp.range('G14').font.color     = '#C00000'
        inp.range('G14').value          = 'Error, bolt outside of section.'
        
        import sys
        sys.exit()
        
    else:
        rowHoriz    = list(np.zeros(len(cxn.rowYcoord)))
        colVert     = list(np.zeros(len(cxn.colXcoord)))
            
        v_1_applied = v_1_cxn / cxn.n_sp
        v_2_applied = v_2_cxn / cxn.n_sp
        
        ecc         = max(cxn.yCoord) - min(cxn.yCoord) + cxn.a_3_group + cxn.clearance
        M_ecc       = -v_2_applied * ecc
        M_applied   = cxn.M_ed 
        
        M_ed        = (M_ecc + M_applied) / cxn.n_sp
        
        for i in list(range(cxn.n_bolts)):
            
            v_1_dir.append(-v_1_applied / cxn.n_bolts)
            v_2_dir.append(v_2_applied  / cxn.n_bolts)
            
            if cxn.yCoord[i] > 0:
                v_2_M.append(M_ed * abs(cxn.yCoord[i]) / cxn.inertiaGroup)
                v_2.append(v_2_dir[-1] + v_2_M[-1])
            
            else: 
                v_2_M.append(-M_ed * abs(cxn.yCoord[i]) / cxn.inertiaGroup)
                v_2.append(v_2_dir[-1] + v_2_M[-1])
                
            if cxn.xCoord[i] < 0:
                v_1_M.append(-M_ed * abs(cxn.xCoord[i]) / cxn.inertiaGroup)            
                v_1.append(v_1_dir[-1] + v_1_M[-1])  
            else:
                v_1_M.append(M_ed * abs(cxn.xCoord[i]) / cxn.inertiaGroup) 
                v_1.append(v_1_dir[-1] + v_1_M[-1])
            
            try: 
                alphaBolt = m.atan(v_2[-1] / v_1[-1])
            except:
                alphaBolt = 0
                
            alpha.append(m.degrees(alphaBolt))
            
            rowHoriz[cxn.rowID[i]]  = rowHoriz[cxn.rowID[i]]    + v_2[-1]
            colVert[cxn.colID[i]]   = colVert[cxn.colID[i]]     + v_1[-1]
            
            v_res.append(( (v_1_dir[-1]+v_1_M[-1])**2 + (v_2_dir[-1] + v_2_M[-1])**2 )**0.5 )
                           
        cxn.maxBoltForce = max(v_res)
        
        cxn.resultant   = v_res
        cxn.v_2         = v_2
        cxn.v_2_abs     = [abs(i) for i in v_2]
        cxn.v_2_dir     = v_2_dir
        cxn.v_2_M       = v_2_M
        cxn.v_1         = v_1
        cxn.v_1_abs     = [abs(i) for i in v_1]
        cxn.v_1_dir     = v_1_dir
        cxn.v_1_M       = v_1_M
        
        cxn.rowHoriz    = rowHoriz
#         print(cxn.rowHoriz)
#         print(cxn.v_1)
#         print(cxn.v_2)
#         print(cxn.v_2_dir)
#         print(cxn.v_2_M)
        cxn.colVert     = colVert
        cxn.alpha       = alpha
        
        pt.vectorField(cxn, el)
        
    return

    
    
