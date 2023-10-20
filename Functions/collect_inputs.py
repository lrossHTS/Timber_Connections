# Collect Excel Inputs function

# Use Excel functions to scrape the key inputs
# Set up output functions

def collect_inputs(input_sheet):   
    inp = input_sheet
    # inp.range('G5','J55').clear()       # Cleans sheet

    try:                                # If plots exist, they are deleted
        inp.pictures['Bolt Plot'].delete()
        inp.pictures['Vec Plot'].delete()
        inp.pictures['Sec Plot'].delete()
    except:
        pass

    # inp.range('G7','J55').font.name = 'Calibri'
    # inp.range('G11').font.bold      = True
    # inp.range('G11').value          = 'Status'
    # inp.range('G12').value          = 'Collecting inputs'

    # Collect element input data
    element_inputs = {
    'input_sheet'       : inp,
    'h'                 : inp.cells(6,13).value,         # depth      
    't'                 : inp.cells(7,13).value,     # element thickness

    # Timber element properties
    'type'              : inp.cells(48,13).value,            # beam or column
    'grade'             : inp.cells(16,13).value,
    'service_class'     : int(inp.cells(17,13).value),                     
    'load_duration'     : inp.cells(18,13).value,          # "Permanent","Long-term","Medium-term","Short-term","Instantaneous"
    'gammaM'            : inp.cells(19,13).value,                 
    'fire_time'         : inp.cells(15,13).value 
    
    }

    # Collect connection input data
    connection_inputs = {
    'calc_ref'          : inp.cells(61,13).value,
    'store_calc'        : inp.cells(62,13).value,
    'grade'             : str(inp.cells(22,13).value),     # 
    'd'                 : inp.cells(23,13).value,          # Fixing diameter (mm)
    'type'              : inp.cells(24,13).value,          # Bolted or dowelled
    'plate_edge'        : inp.cells(51,13).value,          # mm
    'end_clear'         : inp.cells(32,13).value,          # mm

    # Connection Loading:
    'v_1_cxn'           : inp.cells(10,13).value * 10**3,           # v1, N
    'v_2_cxn'           : inp.cells(11,13).value * 10**3,           # v2, N
    'M_ed'              : inp.cells(12,13).value * 10**6,           # Med , Nmm

    # Connection Geometry
    'n_sp'              : inp.cells(30,13).value,          # number of shear planes
    'pl_thk'            : inp.cells(31,13).value,          # flitch plate thickness
    'tolerance'         : inp.cells(7,13).value,           # slot tolerance
    'a_3_group'         : inp.cells(36,13).value,          # Distance to beam end
    'arrangement'       : inp.cells(34,13).value           # "Grid", "Perimeter" or "Circular
    
    }          
        
    # 'loadEcc'           : inp.cells(35,5).value,          # mm ! eccentricity applied in which dir?
        
    if connection_inputs['arrangement'] in ['Grid', 'Perimeter']:
        connection_inputs['a_2']       = inp.cells(42,13).value  
        connection_inputs['a_1']       = inp.cells(41,13).value
        connection_inputs['n_para']    = int(inp.cells(38,13).value)
        connection_inputs['n_perp']    = int(inp.cells(39,13).value)
        
    elif connection_inputs['arrangement'] == 'Circular':
        connection_inputs['radius']    = inp.cells(44,13).value
        connection_inputs['n_bolts']   = int(inp.cells(45,13).value)
        
    if  connection_inputs['type'] == 'Bolted':
        connection_inputs['outerFixing']    = inp.cells(25,13).value
        connection_inputs['recessed']       = inp.cells(54,13).value
        connection_inputs['concealed']      = inp.cells(55,13).value
        
        
        if connection_inputs['outerFixing'] == 'Washer':  
            connection_inputs['washer_d'] = inp.cells(26,13).value
            
        elif connection_inputs['outerFixing'] == 'Plate':
            connection_inputs['fixPlThickness'] = inp.cells(27,13).value
            
    return element_inputs, connection_inputs