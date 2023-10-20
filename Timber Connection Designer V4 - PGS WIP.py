# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:00:20 2023

@author: PSCOTT
"""

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                              TIMBER CONNECTION DESIGNER V4 - PGS WIP                                #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# NOTE:
    # Only import necessary functions from other scripts at the start of the section they will be used in.
    # ...
    # The designer will define or import all of the functions necessary for the connection check, then sets up the classes of the
    # elements, which run the functions needed. Then the elements variables are assigned to a class, and the element outputs are plotted.
    
#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 1   -   SET SHEET AND DIRECTORY        #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Define the starting Excel workbook
# Define the correct directory to work from

import xlwings as xw
import os

# ============================================================================ # 
bk          = xw.Book('Timber Connection Designer.xlsm')
beamInp     = bk.sheets['Beam Designer']
beamInp.range("AA1:FZ500").clear()
colInp   = bk.sheets['Column Designer']
colInp.range("AA1:FZ500").clear()


# ---------------------------------------------------------------------------#
# Change the current working directory if script not located in function file location
funcFileLocation = '\\\\hts-lnd-fs-01\\jobs$\\2564 - HTS+ Tech and data\\4 Calculations\\Python Tools\\02 Timber\\2.1 Timber Connection Designer'
currentDir = os.getcwd()

funcFile_notForCalling = 'J:\2564 - HTS+ Tech and data\4 Calculations\Python Tools\02 Timber\2.1 Timber Connection Designer'

if not funcFile_notForCalling == currentDir:
    os.chdir(funcFileLocation)
    print('Directory changed to function file on server')

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 2   -   GATHER INPUTS & SET UP OUTPUTS #
#------------------------------------------------------------------------------------------------------------------------------------------------#

import Functions.collect_inputs as cinp

beam_element_inputs, beam_connection_inputs = cinp.collect_inputs(beamInp)
col_element_inputs, col_connection_inputs = cinp.collect_inputs(colInp)


#print(element_inputs)

# ---------------------------------------------------------------------------#

import Functions.excel_report as er

# ----------------------------------------------------------------------------#

# --------------------------------------------------------------------------- #
# PLOT TOOLS:
# --------------------------------------------------------------------------- # 

import Functions.plot_tools as pt

def plotBolts(cxn, el):
    pt.plotBolts(cxn, el)
    pt.plotSection(cxn, el)
        
# --------------------------------------------------------------------------- #
# REPORTING TOOLS:
# --------------------------------------------------------------------------- # 
def data_report(cxn):
    er.data_report(cxn)
        
def design_report(cxn):
    er.design_report(cxn)

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 3   -   DEFINE MATERIAL FUNCTIONS        #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Set up functions for primary materials (Timber and Steel)
# Set attributes according to inputs (eg. material properties)
# Set modification factors

# -----------------------------------TIMBER FUNCTIONS----------------------------------------#

import Functions.timber_functions as tf

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 6   -   BOLT ARRANGEMENT AND DESIGN    #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Set up geometry functions of the bolts and sections
# Within this the fire design of the connection (such as recesses) compute

import Functions.connection_geometries as cg

import Functions.bolt_properties as bp

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 8   -   LOADING AND STRESSES           #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Define load variables acting (using inputs)

import Functions.bolt_loads as bl

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 9   -   CAPACITIES                     #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Carry out capacity calcs

import Functions.capacities as cap

def connectionCapacity(cxn, element):
    cxn.F_vRk, cxn.F_vRd              = cap.capacitySteelPlDbleShear(cxn, element)
    cxn.F_vRd_para                    = cap.boltRowReducedCapacity(cxn, element)      
    cxn.F_vRd_perp                    = cap.boltRowPerp(cxn, element)    
    cxn.vEd_cnnxn, cxn.vEd_section    = cap.blockShearStresses(cxn, element)
    
def finPlateCapacity(fin, cxn, element):
   fin.V_Rd_shear                     = cap.finPlateShear(fin, cxn)
   fin.V_Rd_bend                      = cap.finPlateBending(fin, cxn)
   fin.F_Rd_tie                       = cap.finPlateTie(fin, cxn)
   fin.F_bRd_hor, fin.F_bRd_ver       = cap.finBoltBear(fin, cxn)

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 9   -   DESIGN CHECKS                  #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Carry out design checks

import Functions.design_checks as dc

def designChecks(cxn, element):
    dc.initialiseSummary()
        
    # 1 Lateral load capacity
    utilisationArray = dc.check1(cxn)
        
    # 2 Bolt strength parallel to grain
    dc.check2(cxn)
    
    # 3 Splitting in timber
    dc.check3(cxn)
    
    # 4 Block shear in timber
    dc.check4(cxn, element)
    
def finDesignChecks(fin, cxn):
    # Fin plate checks (shear, bending, tying resistance)
    dc.finChecks(fin, cxn)

import Functions.geom_req as gr
    
def geometryChecks(cxn, element):
        
    h = element.h
    
    if cxn.arrangement in ['Grid', 'Perimeter']:
        gr.checkEdgeDistances(cxn, h)
        
    else:
        cxn.geometryStatus = "OK"
        pass      

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 4   -   DEFINE CLASSES AND OBJECTS     #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Set up classes using the functions already defined
# Set Timber first using element_inputs
# Create element object that is a member of timber
# Set Connection class using element and connection_inputs

class Steel:
    def __init__(self):
        self.density    = 7850      # kg/m3
        self.E          = 210000    # N/mm2 
        self.G          = 81000     # N/mm2
        self.f_y        = 355       # N/mm2                 # ASSUMING S355 STEEL FOR NOW
        self.f_u        = 490       # N/mm2                 # ASSUMING S355 STEEL FOR NOW
        self.gamma_M0   = 1.0
        self.gamma_M2   = 1.1    
        
# steel = Steel() # Sets steel as an object that we can input into other classes.  # not necessary, can just use the class directly as an argument.

class Timber:
    def __init__(self, **kwargs):
        # Converts all excel inputs into attributes of the class.
        # ie. 'grade' : "C24" in excel taken by excel_functions as dict item, then converted here to self.grade = "C24"
        for key,value in kwargs.items():
            setattr(self,key,value)
            
        self.output_index           = [4,31]
        self.materialProperties     = tf.materialProperties(self)
        self.timberTypes            = tf.timberTypes(self)
        self.kMod                   = tf.kMod(self)
        #tf.kMod(self)                                  # This option allows just the function to be called, whereas the above method sets the attribute to equal the output of the function. If using this, function just has to set attribute equal to something. If using above, the function must return a value
        self.kDef                   = tf.kDef(self)
        self.k_cr                   = tf.k_cr(self)
        self.charring_rate          = tf.charring_rate(self)
        
        if self.fire_time > 0:
            self.char_depth         = tf.char_depth(self)

beam_element = Timber(**beam_element_inputs)
col_element  = Timber(**col_element_inputs)
#print("The element's kMod is :",element.kMod)

class Connection:
    def __init__(self, element, **kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
            
        self.output_index                   = element.output_index
        self.input_sheet                    = element.input_sheet
                
        if self.type == 'Bolted':
            self.getNetBoltTensArea         = bp.getNetBoltTensArea(self)
        
        self.clearance                      = 10
        self.boltGroupProperties            = cg.boltGroupProperties(self)
        self.k90                            = bp.k90(self, element)
        self.bolt_strength                  = bp.bolt_strength(self)
        self.determineT1                    = cg.determineT1(self, element)
        self.plotBolts                      = plotBolts(self, element)
        self.boltLoads                      = bl.boltLoads(self, element)
        self.geometryChecks                 = geometryChecks(self, element)
        self.connectionCapacity             = connectionCapacity(self, element)
        self.designChecks                   = designChecks(self, element)
        self.data_report                    = data_report(self)                                                       

beam_connection = Connection(beam_element, **beam_connection_inputs)
col_connection = Connection(col_element, **col_connection_inputs)

class FinPlate:
    def __init__(self, material):
       
        for key,value in material.__dict__.items():
            setattr(self,key,value)
        
        self.output_index           = beam_element.output_index
        self.input_sheet            = beam_element.input_sheet
        
        self.b                      = beam_connection_inputs["pl_thk"]                                                               # thickness of plate
        self.d                      = beam_connection.a_2 * (beam_connection.n_para - 1) + 2*beam_connection.plate_edge                        # Depth of plate
        self.ecc                    = max(beam_connection.yCoord) - min(beam_connection.yCoord) + beam_connection.a_3_group + beam_connection.clearance
        #print("ecc is: ", self.ecc)
        self.Lt                     = beam_connection.plate_edge + (beam_connection.n_perp - 1) * beam_connection.a_1 - 0.5 * beam_connection.d     # Length of tension area (block shear)
        self.W_el                   = self.b * self.d**2 / 6
                
        self.finCapacity            = finPlateCapacity(self, beam_connection, beam_element)
        self.finChecks              = finDesignChecks(self, beam_connection) 
        
        
finplate = FinPlate(Steel())


#print(connection.k90)

#------------------------------------------------------------------------------------------------------------------------------------------------#
#                            STEP 10   -   PLOT FINAL RESULTS            #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Use excel writing funcions to write results on the user spreadsheet


er.add_plots(beam_connection)
er.store_report(beam_connection, bk)

er.add_plots(col_connection)
er.store_report(col_connection, bk)

# ---------------------------------------------------------------------------#
# Change directory back
if not funcFile_notForCalling == currentDir:
    os.chdir(currentDir)
    print('Directory changed back')
# ---------------------------------------------------------------------------#

