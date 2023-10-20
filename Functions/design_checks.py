import numpy as np
import Functions.excel_report as er

def initialiseSummary():
    # print("-" * 50)
    # print('Summary of design checks')
    # print("-" * 50)
    return

def check1(cxn):   
    
    resultant = np.array(cxn.resultant)
    F_vRd = np.array(cxn.F_vRd)
    
    utilisationArray = resultant / F_vRd   
    utilisation = max(utilisationArray)
    
    if utilisation < 1:
        status = "Pass"
    else:
        status = "Fail"
    
    cxn.check1 = 'Design status = {} ({}% utilisation)'.format(status, round(utilisation*100))
    
    er.print_result(cxn, 'Check 1 (Fixing capacity)', cxn.check1)
   
    return 

def check2(cxn):   
    
    colVert = np.array(cxn.colVert)
    F_vRd_parallel = np.array(cxn.F_vRd_para)
    
    utilisationArray = abs(colVert) / F_vRd_parallel
     
    utilisation = max(utilisationArray)
    
    if utilisation < 1:
        status = "Pass"
    else:
        status = "Fail"
        
    cxn.check2 = 'Design status = {} ({}% utilisation)'.format(status, round(utilisation*100))
    
    # outputText = 'Design status = {} at {}%'
    
    er.print_result(cxn, 'Check 2 (Bolt row capacity)', cxn.check2)
    
    # print(outputText.format(status, round(utilisation*100)))  
    # print("")
    
    return

def check3(cxn):
    # print("Check 3: Bolt row capacity perpindicular to grain (splitting)")
    
    rowHoriz = np.array(cxn.rowHoriz)
    F_vRd_perpindicular = np.array(cxn.F_vRd_perp)
    
    utilisationArray = abs(rowHoriz) / F_vRd_perpindicular
     
    utilisation = max(utilisationArray)
    
    if utilisation < 1:
        status = "Pass"
    else:
        status = "Fail"
        
    cxn.check3 = 'Design status = {} ({}% utilisation)'.format(status, round(utilisation*100))
    
    er.print_result(cxn, 'Check 3 (Splitting Capacity)', cxn.check3)
    
    # outputText = 'Design status = {} at {}%'
    
    # print(outputText.format(status, round(utilisation*100)))  
    # print("")
    
    return

def check4(cxn, el):
    # print("Check 4: Block shear in section and at connection")
    
    charShearStr = el.f_vk
    designShearStr = charShearStr * el.kMod / el.gammaM
    
    ur_section       = cxn.vEd_section   /   designShearStr
    ur_connection    = cxn.vEd_cnnxn     /   designShearStr
    
    utilisation = max(ur_section, ur_connection)
       
    if utilisation < 1:
        status = "Pass"
    else:
        status = "Fail"
        
    cxn.check4 = 'Design status = {} ({}% at section and {}% at connection)'.format(status, round(ur_section*100), round(ur_connection*100))
    
    er.print_result(cxn, 'Check 4 (Block shear checks)', cxn.check4)
    
    # outputText = 'Design status = {} with {}% at section and {}% at connection'
        
    # print(outputText.format(status, round(ur_section*100), round(ur_connection*100)))  
    # print("")
        
    return

# ---------------------------------------------------------------------------#

# FIN PLATE CHECKS

def finChecks(fin, cxn):
    # Check shear, bending, tie resistance, and bolt bearing utilisation
    
    V_Ed        = cxn.v_2_cxn
    V_Ed_bend   = cxn.v_2_cxn + cxn.M_ed / fin.ecc
    F_Ed        = cxn.v_1_cxn
    F_bEd_hor   = max(cxn.v_2_abs)
    F_bEd_ver   = max(cxn.v_1_abs)
    
    ur_shear = V_Ed / fin.V_Rd_shear
    ur_bend  = V_Ed_bend / fin.V_Rd_bend
    ur_tie   = F_Ed / fin.F_Rd_tie
    ur_bbear = max(F_bEd_hor / fin.F_bRd_hor, F_bEd_ver / fin.F_bRd_ver)
    
    utilisation = max(ur_shear, ur_bend, ur_tie, ur_bbear)
    
    if utilisation < 1:
        status = "Pass"
    else:
        status = "Fail"

    fin.check = 'Design status = {} ({}% in shear, {}% in bending, {}% in tie resistance, {}% in bolt bearing)'.format(status, round(ur_shear*100), round(ur_bend*100), round(ur_tie*100), round(ur_bbear*100))
    
    er.print_result(fin, 'Fin Plate Checks', fin.check)
    
    return




