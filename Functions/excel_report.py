def data_report(cxn):
    output = cxn.input_sheet
    startRow = cxn.output_index[0] + 2
    startCol = cxn.output_index[1]
    
    output.cells(startRow, startCol).value = 'Individual bolt analysis results'
    resultRow = startRow + 1
    
    resultRow = print_bolt_results_title(output, resultRow, startCol)
    
    # output.range((resultRow,27), (100,200)).clear()
    
    # Bolt reporting   
    boltRef = startCol
    xCol    = startCol + 1  
    yCol    = startCol + 2 
    sCol    = startCol + 3
    
    v1dir   = startCol + 4 
    v1M     = startCol + 5
    v1      = startCol + 6
    
    v2dir   = startCol + 7
    v2M     = startCol + 8
    v2      = startCol + 9
    
    alpha   = startCol + 10
    res     = startCol + 11
    
    a_1     = startCol + 12
    a_1_prv = startCol + 13
    
    a_2     = startCol + 14
    a_2_prv = startCol + 15
    
    a_3t    = startCol + 16
    a_3t_prv= startCol + 17
    
    a_3c    = startCol + 18
    a_3c_prv= startCol + 19
    
    a_4t    = startCol + 20
    a_4t_prv= startCol + 21
    
    a_4c    = startCol + 22
    a_4c_prv= startCol + 23
    
    F_vRk   = startCol + 24
    F_vRd   = startCol + 25
    
    for i in range(len(cxn.xCoord)):
                    
        output.cells(resultRow, boltRef).value  = i+1
        output.cells(resultRow, xCol).value     = cxn.xCoord[i]      
        output.cells(resultRow, yCol).value     = cxn.yCoord[i]  
        output.cells(resultRow, sCol).value     = round(cxn.sArray[i],1)

        output.cells(resultRow, v1dir).value    = round(cxn.v_1_dir[i] / 1000,2 )   
        output.cells(resultRow, v1M).value      = round(cxn.v_1_M[i]   / 1000,2 )
        output.cells(resultRow, v1).value       = round(cxn.v_1[i]     / 1000,2 )
        
        output.cells(resultRow, v2dir).value    = round(cxn.v_2_dir[i] / 1000,2 )
        output.cells(resultRow, v2M).value      = round(cxn.v_2_M[i]   / 1000,2 )
        output.cells(resultRow, v2).value       = round(cxn.v_2[i]     / 1000,2 )
                    
        output.cells(resultRow, alpha).value    = round(cxn.alpha[i])
        output.cells(resultRow, res).value      = round(cxn.resultant[i] / 1000,2 )
        
        output.cells(resultRow, a_1).value      = round(cxn.reqs[i].get('a_1') )
        output.cells(resultRow, a_1_prv).value  = round(cxn.dists[i].get('a_1') )        
        output.cells(resultRow, a_2).value      = round(cxn.reqs[i].get('a_2') )
        output.cells(resultRow, a_2_prv).value  = round(cxn.dists[i].get('a_2') )    
        
        try:        # a_3t may not exist
            output.cells(resultRow, a_3t).value     = round(cxn.reqs[i].get('a_3t') )
            output.cells(resultRow, a_3t_prv).value = round(cxn.dists[i].get('a_3t') )
            output.cells(resultRow, a_3c).value     = '-'
            output.cells(resultRow, a_3c_prv).value = '-'
            
        except:     # otherwise, a_3c will exist
            output.cells(resultRow, a_3c).value     = round(cxn.reqs[i].get('a_3c') )
            output.cells(resultRow, a_3c_prv).value = round(cxn.dists[i].get('a_3c') ) 
            output.cells(resultRow, a_3t).value     = '-'
            output.cells(resultRow, a_3t_prv).value = '-'
        
        output.cells(resultRow, a_4t).value     = round(cxn.reqs[i].get('a_4t') )
        output.cells(resultRow, a_4t_prv).value = round(cxn.dists[i].get('a_4t') )        
        output.cells(resultRow, a_4c).value     = round(cxn.reqs[i].get('a_4c') )
        output.cells(resultRow, a_4c_prv).value = round(cxn.dists[i].get('a_4c') )        
                    
        output.cells(resultRow, F_vRk).value    = round(cxn.F_vRk[i] / 1000,1 )
        output.cells(resultRow, F_vRd).value    = round(cxn.F_vRd[i] / 1000,1 )

        resultRow += 1
        
    output.cells(resultRow+1,27).value           = 'Polar Moment of Inertia ='
    output.cells(resultRow+1,28).value           = round(cxn.inertiaGroup)
    output.cells(resultRow+1,29).value           = 'mm2'   

# Row reporting
    resultRow += 3        

    output.cells(resultRow, startCol).value = 'Bolt row analysis'
    resultRow += 1
    
    resultRow = print_row_results_title(output, resultRow, startCol)

    rowRef  = startCol
    n_bolts = startCol + 1
    rowY    = startCol + 2
    rowLoad = startCol + 3
    rowCap  = startCol + 4
    
    for i in range(len(cxn.rowYcoord)):
                    
        output.cells(resultRow, rowRef).value   = i+1
        output.cells(resultRow, n_bolts).value  = cxn.rowID.count(i)
        output.cells(resultRow, rowY).value     = cxn.rowYcoord[i]    

        output.cells(resultRow, rowLoad).value  = round(cxn.rowHoriz[i]  /1000,2)
        output.cells(resultRow, rowCap).value   = round(cxn.F_vRd_perp[i] /1000,2)   
        
        resultRow += 1

# Col reporting
    resultRow += 2    
    output.cells(resultRow, startCol).value = 'Bolt column analysis'
    resultRow += 1

    resultRow = print_col_results_title(output, resultRow, startCol)

    colRef  = startCol
    n_bolts = startCol + 1
    colX    = startCol + 2
    colLoad = startCol + 3
    colCap  = startCol + 4
            
    for i in range(len(cxn.colXcoord)):
                    
        output.cells(resultRow, colRef).value   = i+1
        output.cells(resultRow, n_bolts).value  = cxn.colID.count(i)
        output.cells(resultRow, colX).value     = cxn.colXcoord[i]    
        output.cells(resultRow, colLoad).value  = round(cxn.colVert[i]  /1000,2)
        output.cells(resultRow, colCap).value   = round(cxn.F_vRd_para[i] /1000,2)   
        
        resultRow += 1  
    
    # inp.range('I15').value = u'\u2713' 
        
# ------------------------------------------------------------------------- #     
def add_plots(cxn):
    print('worked')
    cxn.input_sheet.pictures.add(cxn.bolt_plot[0],   name = 'Bolt Plot', update = True,  left = 925)
    cxn.input_sheet.pictures.add(cxn.vec_plot[0],    name = 'Vec Plot',  update = True,  left = 1300, top = 0)
    cxn.input_sheet.pictures.add(cxn.sec_plot[0],    name = 'Sec Plot',  update = True,  left = 1450, top = 0)
        
def print_result(element, title, value):
    R = element.output_index[0]
    C = element.output_index[1]
        
    element.input_sheet.cells(R,C).value    = title
    element.input_sheet.cells(R,C+1).value  = '='
    element.input_sheet.cells(R,C+2).value  = value    
    
    element.output_index[0] += 2
    
def print_bolt_results_title(inp, R,C):
    
    inp.cells(R,C).value = ['Bolt ref']
    inp.cells(R,C+1).value = ['Rel. coordinates']
    inp.cells(R,C+4).value = ['Bolt loads']
    inp.cells(R,C+12).value = ['Geometry requirements']
    inp.cells(R,C+24).value = ['Bolt capacities']
    
    R += 1
    
    inp.cells(R,C+4).value = ['Parallel to grain']   
    inp.cells(R,C+7).value = ['Parallel to grain']   
    inp.cells(R,C+10).value = ['Direction']   
    inp.cells(R,C+11).value = ['Resultant']   
    
    R += 1
    
    inp.cells(R,C+1).value = ['x']
    inp.cells(R,C+2).value = ['y']
    inp.cells(R,C+3).value = ['s']
    inp.cells(R,C+4).value = ['V_1,dir']
    inp.cells(R,C+5).value = ['V_1,mom']
    inp.cells(R,C+6).value = ['V_1']
    inp.cells(R,C+7).value = ['V_2,dir']
    inp.cells(R,C+8).value = ['V_2,mom']
    inp.cells(R,C+9).value = ['V_2']
    inp.cells(R,C+10).value = ['alpha']
    inp.cells(R,C+11).value = ['V']
    inp.cells(R,C+12).value = ['a_1']
    inp.cells(R,C+14).value = ['a_2']
    inp.cells(R,C+16).value = ['a_3t']
    inp.cells(R,C+18).value = ['a_3c']
    inp.cells(R,C+20).value = ['a_4t']
    inp.cells(R,C+22).value = ['a_4c']
    inp.cells(R,C+24).value = ['F_vRk']
    inp.cells(R,C+25).value = ['F_vRd']
        
    R += 1
    
    inp.cells(R,C+12).value = ['req,d']
    inp.cells(R,C+13).value = ['prov,d']
    inp.cells(R,C+14).value = ['req,d']
    inp.cells(R,C+15).value = ['prov,d']
    inp.cells(R,C+16).value = ['req,d']
    inp.cells(R,C+17).value = ['prov,d']
    inp.cells(R,C+18).value = ['req,d']
    inp.cells(R,C+19).value = ['prov,d']
    inp.cells(R,C+20).value = ['req,d']
    inp.cells(R,C+21).value = ['prov,d']
    inp.cells(R,C+22).value = ['req,d']
    inp.cells(R,C+23).value = ['prov,d']
    
    R += 1
    
    inp.cells(R,C+1).value = ['mm']
    inp.cells(R,C+2).value = ['mm']
    inp.cells(R,C+3).value = ['mm2 ?']
    inp.cells(R,C+4).value = ['kN']
    inp.cells(R,C+5).value = ['kN']
    inp.cells(R,C+6).value = ['kN']
    inp.cells(R,C+7).value = ['kN']
    inp.cells(R,C+8).value = ['kN']
    inp.cells(R,C+9).value = ['kN']
    inp.cells(R,C+10).value = ['deg']
    inp.cells(R,C+11).value = ['kN']
    inp.cells(R,C+12).value = ['mm']
    inp.cells(R,C+14).value = ['mm']
    inp.cells(R,C+16).value = ['mm']
    inp.cells(R,C+18).value = ['mm']
    inp.cells(R,C+20).value = ['mm']
    inp.cells(R,C+22).value = ['mm']
    inp.cells(R,C+24).value = ['kN']
    inp.cells(R,C+25).value = ['kN']
    
    R +=1
    
    return R
    
def print_row_results_title(inp, R, C):
    inp.cells(R,C).value = ['Row Ref']
    inp.cells(R,C+1).value = ['No bolts']
    inp.cells(R,C+2).value = ['Rel. coordinate']
    inp.cells(R,C+3).value = ['Row loads']
    inp.cells(R,C+4).value = ['Row capacity']
    
    R += 1
    
    inp.cells(R,C+2).value = ['y']
    inp.cells(R,C+4).value = ['F_vRd,2']
    
    R += 1
    
    inp.cells(R,C+2).value = ['mm']
    inp.cells(R,C+3).value = ['kN']
    inp.cells(R,C+4).value = ['kN']
    
    R +=1
    
    return R

def print_col_results_title(inp, R, C):
    inp.cells(R,C).value = ['Col Ref']
    inp.cells(R,C+1).value = ['No bolts']
    inp.cells(R,C+2).value = ['Rel. coordinate']
    inp.cells(R,C+3).value = ['Col loads']
    inp.cells(R,C+4).value = ['Col capacity']
    
    R += 1
    
    inp.cells(R,C+2).value = ['x']
    inp.cells(R,C+4).value = ['F_vRd,1']
    
    R += 1
    
    inp.cells(R,C+2).value = ['mm']
    inp.cells(R,C+3).value = ['kN']
    inp.cells(R,C+4).value = ['kN']
    
    R +=1
    
    return R
    
# ---------------------------------------------------------------------------#

def print_error(element, error_message):
    R = element.output_index[0]
    C = element.output_index[1]
        
    element.input_sheet.cells(R,C).value    = "Error"
    element.input_sheet.cells(R,C+2).value  = error_message   
    
    import sys
    sys.exit()
 
# ---------------------------------------------------------------------------#    
 
def store_report(cxn, bk): 
    # store_report_choice = slab.input_sheet.range('F51').value   
    # calculation_reference = slab.input_sheet.range('F49').value     
    
    store_report_choice = cxn.store_calc
    print(store_report_choice)
    calculation_reference = cxn.calc_ref
    
    print('worked')
    
    # print(store_report_choice)
    worksheets = bk.sheets
    
    copy_ref = 1
    
    for s in worksheets:
        if s.name == calculation_reference:

            if s.name[-1] == ')':
                calculation_reference = calculation_reference[0:-4]
                calculation_reference = calculation_reference + ' (' + str(copy_ref) + ')'                
            else:
                calculation_reference = calculation_reference + ' (' + str(copy_ref) + ')'
                
            copy_ref = copy_ref + 1

        
    if store_report_choice == 'Y':
        print('worked')
        cxn.input_sheet.copy(name = calculation_reference)
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        