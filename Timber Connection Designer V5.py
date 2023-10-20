# Import functions
import xlwings as xw
import os
import Functions.collect_inputs as cinp
import Functions.excel_report as er
import Functions.plot_tools as pt
import Functions.timber_functions as tf
import Functions.connection_geometries as cg
import Functions.bolt_properties as bp
import Functions.bolt_loads as bl
import Functions.capacities as cap
import Functions.design_checks as dc
import Functions.geom_req as gr
import Classes.connection_class as cc

# Initialise excel workbook
bk          = xw.Book('Timber Connection Designer.xlsm')
beamInp     = bk.sheets['Beam Designer']
beamInp.range("AA1:FZ500").clear()
colInp   = bk.sheets['Column Designer']
colInp.range("AA1:FZ500").clear()

# Change directory stuff
# See WSH append path for this. 

connection = cc.Connection

# 1. Initialise connection as fin-fin connection
# 2. Define supported member as a beam
# 3. Set supported member type as timber
# 4. Set connection geometry at supported member
# 5. Apply loadcase to connection

# --------------------------------------------------------- # 

beam_element_inputs, beam_connection_inputs = cinp.collect_inputs(beamInp)
col_element_inputs, col_connection_inputs = cinp.collect_inputs(colInp)

beam_element = Timber(**beam_element_inputs)
col_element  = Timber(**col_element_inputs)                                    

beam_connection = Connection(beam_element, **beam_connection_inputs)
col_connection = Connection(col_element, **col_connection_inputs)