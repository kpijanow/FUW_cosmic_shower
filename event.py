"""
project: FUW_cosmic_shower
    event.py
for each event: 
coincidence of detected muons
for coincidence > 2: direction of incoming cosmic shower
"""

import constants 
import numpy as np
import math as math


class Event():
    
    def __init__(self, line):
        self.const = constants.Constants()
        self.t1 = np.array(line[0:4]) 
        self.t2 = np.array(line[4:8])
        self.time = line[8]        
##        self.ToT = [j-i for i,j in zip (self.t1, self.t2)]
        self.detectorsFired = [0, 0, 0, 0]
        self.arrivalTimes = [0, 0, 0, 0]
        self.nMuons = self.coincidence()
        self.radius = self.getRadius()
        self.vector = None
        self.zenith = self.getZenith()
        
    def coincidence(self):
        for i in range(4):
            if self.t1[i]!=-1:
                self.detectorsFired[i] = 1
                self.arrivalTimes[i] = self.t1[i]
            else:
                self.detectorsFired[i] = 0
                self.arrivalTimes[i] = 0
                
        return np.sum(self.t1 != -1) #if we are using only t1 than coincidence should be nr of
                                     #times that t1 was read properly
    
    def getRadius(self):
        if self.nMuons >= 2:
            self.detecotrsFired = self.t1 != -1
            i = np.nonzero(self.t1 != -1)
            dx = []
            for j in range(self.nMuons):
                for k in range(self.nMuons):
                    dx.append(self.const.det_X[i[0][j]] - self.const.det_X[i[0][k]])
            return max(dx)
        else: return 0

    def getZenith(self):
        #temp = self.t1[0]
        #self.t1[0] = self.t1.max()
        #self.t1[self.t1.argmax()] = temp
        try:
            if self.nMuons >= 2:
                self.detecotrsFired = self.t1 != -1
                i = np.nonzero(self.t1 != -1)
                v1 = [self.radius, 0]
                vector = [0, 0, 0]
                            #if(self.const.v_muon * math.abs(self.t1[i[0][1]] - self.t1[i[0][0]] > 
                vector[2] = min(1, max(self.const.v_muon * abs(self.t1[i[0][1]] - self.t1[i[0][0]])/v1[0], -1))
                vector[2] = math.asin(vector[2])
                zenith = vector[2]
                vector[2] = 1/math.sqrt((1 + math.tan(zenith)*math.tan(zenith)))
                vector[0] = vector[2] * math.tan(zenith)

                self.vector = vector
                zenith = math.degrees(zenith)
                return zenith
            else: return 0
        except:
            return 0
        
    def getDirection(self):
        #temp = self.t1[0]
        #self.t1[0] = self.t1.max()
        #self.t1[self.t1.argmax()] = temp
        if self.nMuons >= 2:
            self.detecotrsFired = self.t1 != -1
            i = np.nonzero(self.t1 != -1)
            
            v1 = [self.radius, 0]
            vector = [0, 0, 0]

            vector[2] = min(1, max(self.const.v_muon * abs(self.t1[i[0][1]] - self.t1[i[0][0]])/math.sqrt(v1[0]*v1[0] + v1[1]*v1[1]), -1))
            vector[2] = math.asin(vector[2])
            
            vector[2] = math.tan(vector[2])
            vector[2] = vector[2]*(math.sqrt(v1[0]*v1[0] + v1[1]*v1[1]))
            vector[0] = v1[0]/math.sqrt(v1[0]*v1[0] + v1[1]*v1[1] + vector[2]*vector[2])
            vector[1] = v1[1]/math.sqrt(v1[0]*v1[0] + v1[1]*v1[1] + vector[2]*vector[2])
            vector[2] = vector[2]/math.sqrt(v1[0]*v1[0] + v1[1]*v1[1] + vector[2]*vector[2])
            return vector

        elif self.nMuons == 3:
            self.detecotrsFired = self.t1 != -1
            i = np.nonzero(self.t1 != -1)
            v1 = [self.const.det_X[i[0][1]] - self.const.det_X[i[0][0]],
                  self.const.det_Y[i[0][1]] - self.const.det_Y[i[0][0]] ]
            
            v2 = [self.const.det_X[i[0][2]] - self.const.det_X[i[0][0]],
                  self.const.det_Y[i[0][2]] - self.const.det_Y[i[0][0]] ]
            if v2[1] != 0:
                a = [self.const.v_muon * (self.t1[i[0][1]] - self.t1[i[0][0]]), self.const.v_muon * (self.t1[i[0][2]] - self.t1[i[0][0]])]

                vector = [0, 0, 0]
                if v1[1] * v2[0] - v1[0] * v2[1] != 0:
                    vector[0] = -(a[1] * v1[1] - a[0] * v2[1])/(v1[0] * v2[1] - v1[1] * v2[0])
                    vector[1] = (a[1] * v1[0] - a[0] * v2[0])/(v1[0] * v2[1] - v1[1] * v2[0])
                else:
                    vector = [0, 0, 1]   

                if (vector[0]**2 + vector[1]**2) < 1:
                    vector[2] = math.sqrt(1 - vector[0]**2 - vector[1]**2)
                else:
                    vector = [0, 0, 1]
                return vector
        elif self.nMuons == 4:
            self.detecotrsFired = self.t1 != -1
            vector = np.zeros(3)
            
            for iRef in range(4):
                iD1 = (iRef + 1)%4
                iD2 = (iRef + 3)%4
                
                v1 = [self.const.det_X[iD1] - self.const.det_X[iRef],
                      self.const.det_Y[iD1] - self.const.det_Y[iRef] ]
            
                v2 = [self.const.det_X[iD2] - self.const.det_X[iRef],
                      self.const.det_Y[iD2] - self.const.det_Y[iRef] ]
            
                a = [self.const.v_muon * (self.t1[iD1] - self.t1[iRef]), self.const.v_muon * (self.t1[iD2] - self.t1[iRef])]
                vectorTemp = np.zeros(3)

                if v1[1] * v2[0] - v1[0] * v2[1] != 0:
                    vectorTemp[0] = -(a[1] * v1[1] - a[0] * v2[1])/(v1[1] * v2[0] - v1[0] * v2[1])
                    vectorTemp[1] = (a[1] * v1[0] - a[0] * v2[0])/(v1[1] * v2[0] - v1[0] * v2[1])
                else:
                    vectorTemp = [0, 0, 1]
                    
                if (vectorTemp[0]**2 + vectorTemp[1]**2) < 1:
                    vectorTemp[2] = math.sqrt(1 - vectorTemp[0]**2 - vectorTemp[1]**2)
                else:
                    vectorTemp = [0, 0, 1]
                
                vector = vector + vectorTemp

            return vector/4.0
        else:
            return None
