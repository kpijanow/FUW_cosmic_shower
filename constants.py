class Constants:
    
    def __init__(self):
        self.cable_length = 15
        self.det_X = self.calbelength * [1, 1, -1, -1]
        self.det_Y = self.cable_length * [1, -1, -1, 1]
        self.det_area = 0.31 * 0.27
        self.readOut_eff = 0.95
        self.det_eff = 0.75

    def getDet_X(self):
        return self.det_X

    def getDet_Y(self):
        return self.det_Y

    def getDet_area(self):
        return self.det_area

    def getDet_eff(self):
        return self.det_eff

    def getReadOut_eff(self):
        return self.readOut_eff

    def setDet_X(self, det_X0):
        self.det_X = det_X0

    def setDet_Y(self, det_Y0):
        self.det_Y = det_Y0
    
