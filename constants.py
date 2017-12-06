import numpy as np

class Constants:  
    def __init__(self):
        self.cable_length = 0.5
        self.det_X = self.cable_length/(2**(1/2)) * np.array([1.0, 1.0, -1.0, -1.0])
        self.det_Y = self.cable_length/(2**(1/2)) * np.array([1.0, -1.0, -1.0, 1.0])
        #self.det_Z = [1, 1, 1, 1]
        self.det_area = 0.31 * 0.27
        self.readOut_eff = 0.95
        self.det_eff = 0.75
        self.v_muon = 0.298 # 29.8 cm/ns from https://paulba.no/paper/Liu.pdf

    def getDet_X(self):
        """list of X positions of all 4 detectors"""
        return self.det_X

    def getDet_Y(self):
        """list of Y positions of all 4 detectors"""
        return self.det_Y

    def getDet_area(self):
        """area of a single detecotr"""
        return self.det_area

    def getDet_eff(self):
        """detector efficiency"""
        return self.det_eff

    def getReadOut_eff(self):
        """readout efficiency i.e. procentage of events that 
        were read correctly"""
        return self.readOut_eff

    def setDet_X(self, det_X0):
        """set the X positions of all 4 detectors"""
        self.det_X = det_X0

    def setDet_Y(self, det_Y0):
        """set the Y positions of all 4 detectors"""
        self.det_Y = det_Y0
    
