# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:58:15 2023

@author: PSCOTT
"""

import numpy as np
import math as m
import Functions.plot_tools as pt

# --------------------------------------------------------------------------- # 
def axialCapBolt(cxn, el):
    # Calculation of bolt axial capacity for determination of rope effect
    # Axial capacity is minimum of:
    # bolt tensile capacity / bearing capacity of washer / bearing capacity of plate
    
    # 1) Bolt tensile capacity
    gammaM2             = 1.25
    tensCapChar         = 0.9 * cxn.f_uk * cxn.A_boltNet
    tensCapDes          = tensCapChar / gammaM2
       
    if cxn.outerFixing == 'Washer':
        # 2) Washer capacity
        washerArea      = m.pi * (cxn.washer_d/2) **2 - m.pi * (cxn.d/2 +1)**2
        timbCompCapChar = 3 * washerArea * el.f_c90k                                    # 8.5.2(2)
        timbCompCapDes  = timbCompCapChar * el.kMod / el.gammaM
        
        F_axRk          = min(tensCapChar, timbCompCapChar)
    
    elif cxn.outerFixing == 'Plate':
        # 3) Plate capacity
        dia_pl          = min(12 * cxn.fixPlThickness, 4 * cxn.d)                 # 8.5.2(3) max bearing dia of plate
        A_pl            = m.pi * (dia_pl/2) **2 - m.pi * (dia_pl/2 +1)**2
        timbCompCapChar = 3 * A_pl * el.f_c90k 
        timbCompCapDes  = timbCompCapChar * el.kMod / el.gammaM

        F_axRk          = min(tensCapChar, timbCompCapChar)
    
    return F_axRk

# --------------------------------------------------------------------------- # 
def capacitySteelPlDbleShear(cxn, el):
    alpha               = np.array(cxn.alpha)
    alpha               = np.radians(cxn.alpha)
 
    timbDens            = el.rho_mean
    boltDia             = cxn.d
    k_90                = cxn.k_90
    t1                  = cxn.t1
    
    # Applicable for embedded steel double shear connection
    # Char fastener yield moment
    M_yRk               = 0.3 * cxn.f_uk * boltDia**2.6   # Nmm 
    
    # Char withdrawal capacity of fastener (Assume zero for dowel)
    if cxn.type == 'Bolted':
        F_axRk          = axialCapBolt(cxn, el)
    
    elif cxn.type == 'Dowelled':
        F_axRk = 0 
        
    F_vRd               = []
    F_vRk               = []
    
    # Char embedment strength // to grain
    f_h0k               = (0.082*(1-0.01 * boltDia) * timbDens)                 # MPa 
    # print('f_h0k = ', round(f_h0k), " MPa")
    
    for i in range(len(cxn.xCoord)):
        # Char embedment strength at angle, A, to grain
        f_hk            = f_h0k / (cxn.k_90 * m.sin(alpha[i])**2 + m.cos(alpha[i])**2)   # MPa
    
        # Steel in double shear
        # Char load capacity per shear plane, per fastener
        F_vrk1          = f_hk * t1 * boltDia                # 8.2.3 (c)
        
        F_vrk2_johans   = f_hk * t1 * boltDia * (( 2 + (4 * M_yRk) / (f_hk * boltDia * t1**2))**0.5 - 1) # 8.2.3(d)
        F_vrk2_rope     = min(F_vrk2_johans/4 , F_axRk/4)                           # check rope effect < 25% of johansen yield (8.2.2(2))
        F_vrk2          = F_vrk2_johans + F_vrk2_rope                                    
        
        F_vrk3_johans   = 2.3 * (M_yRk * f_hk * boltDia)**0.5                         # 8.2.3(e)
        F_vrk3_rope     = min(F_vrk3_johans/4,  F_axRk / 4)                         # check rope effect < 25% of johansen yield
        F_vrk3          = F_vrk3_johans + F_vrk3_rope
           
        F_vRk.append(min(F_vrk1, F_vrk2, F_vrk3))   
        # print("The Fv_Rk in capacities is:",F_vRk)                            # eq 8.10
        F_vRd.append(F_vRk[-1] * el.kMod / el.gammaM)
    
    return F_vRk, F_vRd

# --------------------------------------------------------------------------- # 
def boltRowReducedCapacity(cxn, el):
    #   Calculate effective number of bolts in row parallel to grain (Eq 8.34)
    #   Note: Assumes vert spacing equal in all instances. Not correct for perimeter or circular arranagement. 
    
    F_vRd_parallel = []
    F_vRk = min(cxn.F_vRk)
    
    for i in range(len(cxn.colXcoord)):
        
        n_row = cxn.colID.count(i)       
        n_efRow = min( n_row, n_row**0.9 * ( cxn.a_1 / (13 * cxn.d) )**0.25 )

        F_vRd_parallel.append(n_efRow * F_vRk * el.kMod / el.gammaM)
        
    return F_vRd_parallel

# --------------------------------------------------------------------------- # 
def boltRowPerp(cxn, el):
    #   Calculates capacity to resist splitting (8.1.4)
    
    if el.timberType == "Softwood":
        
        F_vRd_perpindicular = []
        
        w = 1                           # Modification factor
        h = el.h                        # Assign variable to match Eurocode documentation
        b = cxn.t1                      # Assign variable to match Eurocode documentation
               
        for i in range(len(cxn.rowYcoord)):
            
            # Find max xCoord for boltRow to calc h_e
            xCoordOuterBolt = 0
            
            for j in range(len(cxn.rowID)): 
                rowIndex = cxn.rowID[i]
                
                if rowIndex == cxn.rowID[j] and abs(cxn.xCoord[j]) > xCoordOuterBolt:
                    xCoordOuterBolt = abs(cxn.xCoord[j])
            
            h_e = h/2 + xCoordOuterBolt
            
            F_90Rk = 14 * b * w * (h_e / (1 - h_e/h)) **0.5
            
            F_vRd_perpindicular.append(F_90Rk * el.kMod / el.gammaM)
            
    else:
        print("Timber type not OK. F_90,Rk equation (8.4) only suitable for softwoods")
         
    return F_vRd_perpindicular

# --------------------------------------------------------------------------- # 
def blockShearStresses(cxn, el):
    # Return shear stress within connection area and max shear stress outside of connection area.
    
    shearStressBoltRow = []
    
    # shear stress at each bolt row:
    b = cxn.t1              # width of timber at shear area
    d = el.h           # depth of timber at shear area
    shearForce = cxn.v_2_cxn / 2      # extract perp shear
        
    for i in range(len(cxn.rowYcoord)):
            
        shearForce = abs(cxn.rowHoriz[0])
        noBoltsInRow = cxn.rowID.count(i)       # Count number of bolts in row
        shearArea = (d - noBoltsInRow * (cxn.d+1)) * b
        shearStress = 3/2 * shearForce / shearArea
        
        shearStressBoltRow.append(shearStress)
        
    maxShearAtBoltRow = max(shearStressBoltRow)
    
    # shear stress at section:
    b = cxn.t1
    d = el.h 
    shearArea = b * d
    
    timberShearStress = 3/2 * shearForce / shearArea

    return maxShearAtBoltRow, timberShearStress

# --------------------------------------------------------------------------- # 
def finPlateShear(fin, cxn):
    # Calculates capacity of fin plate in shear, checking gross, net, and block shear
    
    Avnet = fin.b*(fin.d - cxn.n_para * cxn.d)
    Anv   = fin.b * (fin.d - cxn.plate_edge - (cxn.n_para - 0.5) * cxn.d)
    Ant   = fin.Lt - (cxn.n_perp - 0.5) * cxn.d
    
    V_Rdg = fin.b * fin.d * fin.f_y / (1.27 * (3**0.5) * fin.gamma_M0)
    V_Rdn = Avnet * fin.f_u / ((3**0.5) *fin.gamma_M0)
    V_Rdb = fin.f_u * Ant / (2*fin.gamma_M2)  +  fin.f_y * Anv / ((3**0.5) * fin.gamma_M0)
    
    shearcaps = [V_Rdg, V_Rdn, V_Rdb]
    
    V_Rd_shear = min(shearcaps)
    
    return V_Rd_shear

# --------------------------------------------------------------------------- # 
def finPlateBending(fin, cxn):
    # Calculates capacity of fin plate in bending
    
    if fin.d >= 2.73 * fin.ecc:
        V_Rd_bend = cxn.v_2_cxn * 1000          # Arbitrarily high value because it always passes.
    
    else:
        V_Rd_bend = fin.W_el * fin.f_y / (fin.ecc * fin.gamma_M0)
        
    return V_Rd_bend

# --------------------------------------------------------------------------- # 
def finPlateTie(fin,cxn):
    # Calculates tying resistance of the fin plate.
    Anet = fin.b*(fin.d - cxn.n_para * cxn.d)    
    Anv  = fin.b * (fin.d - cxn.plate_edge - (cxn.n_para - 0.5) * cxn.d)
    Ant  = fin.Lt - (cxn.n_perp - 0.5) * cxn.d
    
    F_Rdn = 0.9 * Anet * fin.f_u / fin.gamma_M2
    F_Rdb = fin.f_u * Ant / fin.gamma_M2  +  fin.f_y * Anv / ((3**0.5) * fin.gamma_M0)
    
    tiecaps = [F_Rdb, F_Rdn]
    
    F_Rd = min(tiecaps)
    
    return F_Rd


# --------------------------------------------------------------------------- # 
def finBoltBear(fin,cxn):
    # Calculates bearing capacity of bolts on the fin plate.
    # Find the capcity in hor. and ver., and then compares to the worst case in each directio nin 'design_checks'
    
    gammaM = 1.25
    f_ubolt = 800 # Ultime tensile strength of 8.8 bolt acc. to EN1993-1-8 Table 3.1
    
    # Vertical capacity
    
    k1_ver = min(2.8*cxn.plate_edge/cxn.d -1.7, 1.4*cxn.a_1/cxn.d - 0.25, 2.5)
    a_b_ver = min(cxn.plate_edge/(3*cxn.d), cxn.a_2/(3*cxn.d) - 0.25, f_ubolt/fin.f_u, 1)
    F_bRd_ver = k1_ver * a_b_ver * fin.f_u * cxn.d * fin.b / gammaM
    
    # Horizontal capacity
    
    k1_hor = min(2.8*cxn.plate_edge/cxn.d -1.7, 1.4*cxn.a_2/cxn.d - 1.7, 2.5)
    a_b_hor = min(cxn.plate_edge/(3*cxn.d), cxn.a_1/(3*cxn.d) - 0.25, f_ubolt/fin.f_u, 1)
    F_bRd_hor = k1_hor * a_b_hor * fin.f_u * cxn.d * fin.b / gammaM    
    
    return F_bRd_hor, F_bRd_ver
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
