class Connection:
    def __init__(self):
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

        def geometryChecks(cxn, element):
            h = element.h
            
            if cxn.arrangement in ['Grid', 'Perimeter']:
                gr.checkEdgeDistances(cxn, h)
                
            else:
                cxn.geometryStatus = "OK"
                pass      
            
        def connectionCapacity(cxn, element):
            cxn.F_vRk, cxn.F_vRd              = cap.capacitySteelPlDbleShear(cxn, element)
            cxn.F_vRd_para                    = cap.boltRowReducedCapacity(cxn, element)      
            cxn.F_vRd_perp                    = cap.boltRowPerp(cxn, element)    
            cxn.vEd_cnnxn, cxn.vEd_section    = cap.blockShearStresses(cxn, element)

        def plotBolts(cxn, el):
            pt.plotBolts(cxn, el)
            pt.plotSection(cxn, el)
        
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
        
    def finPlateCapacity(self, cxn, element):
        self.V_Rd_shear                     = cap.finPlateShear(self, cxn)
        self.V_Rd_bend                      = cap.finPlateBending(self, cxn)
        self.F_Rd_tie                       = cap.finPlateTie(self, cxn)
        self.F_bRd_hor, self.F_bRd_ver       = cap.finBoltBear(self, cxn)

    def finDesignChecks(fin, cxn):
        # Fin plate checks (shear, bending, tying resistance)
        dc.finChecks(fin, cxn)