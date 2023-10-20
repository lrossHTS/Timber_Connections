# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:48:54 2023

@author: PSCOTT
"""

import Functions.excel_report as er

# def bolt_strength(cxn):
#     grade = cxn.grade
        
#     boltStrengthList = {'4.6': {'f_yk': 240, 'f_uk':400},
#                         '4.8': {'f_yk': 240, 'f_uk':400},
#                         '5.6': {'f_yk': 240, 'f_uk':400},
#                         '6.8': {'f_yk': 240, 'f_uk':400},
#                         '8.8': {'f_yk': 240, 'f_uk':400},
#                         '10.9':{'f_yk': 240, 'f_uk':400}}
    
#     cxn.f_uk = boltStrengthList[grade]['f_uk']
#     cxn.f_yk = boltStrengthList[grade]['f_yk']
    
#     er.print_result(cxn, 'Ultimate fixing strength',       cxn.f_uk)
#     er.print_result(cxn, 'Char. fixing yield strength',    cxn.f_yk)
    
# --------------------------------------------------------------------------- #
# def k90(cxn, element):
        
#     if element.grade in ["C16", "C24", "C27", "GL24c", "GL28c", "GL32c", "GL24h", "GL28h", "GL32h", "GL75"]:
#         cxn.k_90 = 1.35 + 0.015 * cxn.d
#     else:
#         print("Grade not supported")
#         cxn.k_90 = None 
        
#     er.print_result(cxn, 'k_90',    cxn.k_90)
    
# --------------------------------------------------------------------------- #           
# def getNetBoltTensArea(cxn):
#     boltDiaList = [   5,    6,    7,    8, 10, 12,    14,  16,  18,  20,  22,  24,  27,  30]
#     netAreaList = [14.2, 20.1, 28.9, 36.6, 58, 84.3, 115, 157, 192, 245, 303, 353, 459, 561]
    
#     d = cxn.d
    
#     if d in boltDiaList:
#         cxn.A_boltNet = netAreaList[boltDiaList.index(d)]   
#     else:
#         print('Bolt diameter not supported')
        
#     er.print_result(cxn, 'Net bolt tensile area', cxn.A_boltNet)