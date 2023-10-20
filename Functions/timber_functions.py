# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:11:50 2023

@author: PSCOTT
"""
import Functions.excel_report as er

def timberTypes(timber):
        
    softwoodList    = ["C16", "C24", "C27"] 
    glulamList      = ["GL24c", "GL28c", "GL32c", "GL24h", "GL28h", "GL32h", "GL75" ]
        
    # Note:
    # Material type for kDef and kMod
    # Timber type for k_90 in bolt capacity calculation
    # Grade is taken from excel inputs by excel functions
    
    if timber.grade in softwoodList:
        timber.materialType = "Solid Timber"
        timber.timberType = "Softwood"
        
    elif timber.grade in glulamList:
        timber.materialType = "Glulam"
        timber.timberType = "Softwood"
        
    else: 
        timber.materialType = None
        timber.timberType = None
        print("Material grade not yet supported")
        
    er.print_result(timber, 'material type', timber.materialType )
    er.print_result(timber, 'timber type', timber.timberType )
        
 # --------------------------------------------------------------------------- #    
def k_cr(timber):
    if timber.materialType == "Glulam" or timber.materialType == "Solid Timber":  
        kCr = 0.67
        
    else:
        kCr = 1      
    
    return kCr
    
    er.print_result(timber, 'k_cr', kCr )      
        
# --------------------------------------------------------------------------- #         
def kMod(timber):
    if not timber.materialType in ["Glulam" ,"Solid Timber" ,"LVL"]:
        print("Material type Plywood, OSB and Particle board not yet included")
        print("Or check material type input")    
        
        timber.kMod = None
        
    # Load duration and Service Class is taken from excel inputs by excel functions
    
    else:
        LDClassList = ["Permanent","Long-term","Medium-term","Short-term","Instantaneous"]
        
        kModIndex = LDClassList.index(timber.load_duration)
        
        kModArray = [[0.6, 0.7, 0.8, 0.9, 1.1],
                     [0.6, 0.7, 0.8, 0.9, 1.1],
                     [0.5,0.55, 0.65, 0.7, 0.9]]        
        
        #timber.kMod = kModArray[timber.service_class-1][kModIndex]
        # print("The kMod from timber_functions is:", timber.kMod)
        kMod = kModArray[timber.service_class-1][kModIndex]
        
        er.print_result(timber, 'k_mod', kMod )
     
    return kMod
        
# --------------------------------------------------------------------------- # 
def kDef(timber):
    if not timber.materialType in ["Glulam" ,"Solid Timber" ,"LVL"]:
        print("Material type Plywood, OSB and Particle board not yet included")
        print("Or check material type input")    
        
        timber.kDef = None
        
    else:
        kDefList = [0.6, 0.8, 2.00]            
        timber.kDef = kDefList[timber.service_class-1]        
        
    er.print_result(timber, 'k_def', timber.kDef )
        
# --------------------------------------------------------------------------- #     
def materialProperties(timber):
    matPropList = ["C16", "C24", "C27", "GL24c", "GL28c", "GL32c", "GL24h", "GL28h", "GL32h", "GL75" ]
    matPropIndex = matPropList.index(timber.grade)
        
    k_hm = (600/timber.h)**0.10
    k_ht = (600/timber.h)**0.10
    k_hv = (600/timber.h)**0.13
        
    matPropArray =      [[16,       8.5,        2.2, 17,   2.2,     3.2,        8000,  5400,  270, 500, 370, 310],
                         [24,       14.5,       2.5, 21,   2.5,     4.0,        11000, 7400,  370, 690, 420, 350],
                         [27,       16.5,       2.5, 22,   2.5,     4.0,        11500, 7700,  380, 720, 430, 370],
                         [24,       17,         0.5, 21.5, 2.5,     3.5,        11000, 9100,  300, 650, 400, 365],
                         [28,       19.5,       0.5, 24,   2.5,     3.5,        12500, 10400, 300, 650, 420, 390],
                         [32,       19.5,       0.5, 24.5, 2.5,     3.5,        13500, 11200, 300, 650, 440, 400],
                         [24,       19.2,       0.5, 24,   2.5,     3.5,        11500, 9600,  300, 650, 420, 385],
                         [28,       22.3,       0.5, 28,   2.5,     3.5,        12600, 10500, 300, 650, 460, 425],
                         [32,       25.6,       0.5, 32,   2.5,     3.5,        14200, 11800, 300, 650, 490, 440],
                         [k_hm*75,  k_ht*60,    0.6, 49.5, 12.3,    k_hv*4.5,   16800, 15300, 470, 850, 850, 730]]
    
    timber.f_mk       = matPropArray[matPropIndex][0]
    timber.f_t0k      = matPropArray[matPropIndex][1]
    timber.f_t90      = matPropArray[matPropIndex][2]
    timber.f_c0k      = matPropArray[matPropIndex][3]
    timber.f_c90k     = matPropArray[matPropIndex][4]
    timber.f_vk       = matPropArray[matPropIndex][5]
    timber.E_0mean    = matPropArray[matPropIndex][6]
    timber.E_005      = matPropArray[matPropIndex][7]
    timber.E_90mean   = matPropArray[matPropIndex][8]
    timber.G_mean     = matPropArray[matPropIndex][9]
    timber.rho_mean   = matPropArray[matPropIndex][10]
    timber.rho_k      = matPropArray[matPropIndex][11]       
# --------------------------------------------------------------------------- #
def charring_rate(timber):
    beta_m_dict = {'Solid Timber':      0.7, 
                   'Glulam':            0.8,
                   'Light Hardwood':    0.7,
                   'Dense Hardwood':    0.55,
                   'LVL':               0.7}
        
    timber.beta_m = beta_m_dict[timber.materialType]
    
    er.print_result(timber, 'charring rate, beta_m', timber.beta_m )
        
# --------------------------------------------------------------------------- #
def char_depth(timber):
    d_0 = 7                                     # mm
    
    # Fire time is taken from excel inputs by excel functions
    
    if timber.fire_time > 0:                 
        d_char_n = timber.beta_m * timber.fire_time
        timber.d_char_ef = d_char_n + d_0
        
        er.print_result(timber, 'char depth, d_char_ef', timber.d_char_ef )        