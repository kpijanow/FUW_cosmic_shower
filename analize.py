import constants 
import readout
import numpy as np
import math as math
import threading

detectedMuons = 0

class Event(constants.Constants):

    def __init__(self, line):
        self.t1 = np.array(line[0:4]) ## ??
        self.t2 = np.array(line[4:])
        self.time = 0 
        #self.time = line[8]        # TO DO: add global time to readout.py
        self.ToT = [j-i for i,j in zip (self.t1, self.t2)]
        self.nMuons = self.Coincidence()
        self.vector = self.Direction()
        self.Flux()
        
    

    def Coincidence(self):
        n = 0
        for i in range(4):
            if self.ToT:
                n+=1
        return n

    def Flux(self):
        global detectedMuons
        detectedMuons += self.nMuons

##----------------------------------------------
##    vectors start here and it's crap
##----------------------------------------------    
    def getPoint(self, n):                                ## ooops
##        rho = Constants.c*t1[n]
##        p = np.array([Constants.det_X[n], Constants.det_Y[n], 0])
##        v = p - p0
##        distance = math.sqrt(sum(j**2 for j in v))
##        theta = math.pi/2 - math.acos(rho/distance)
##        z = distance*math.tan(theta)
        p = np.array([constants.det_X[n], constants.det_Y[n], self.t1[n]])
##        p = np.array([Constants.det_X[n], Constants.det_Y[n], z])
        return p

    def Direction(self):
        if self.nMuons < 3:
            return 0
        else:            
##            t = np.array(self.t1)           
            t_min = np.argpartition(self.t1,2)    ## where was the first hit -> this is our reference
            if self.t1[t_min[:2]][0]==0:
                t_first = t1[t_min[:2][1]]      ##  reference for exaple to t1 as self.t1
            else:
                t_first = t1[t_min[:2][0]]
            [firstDet], = np.where(t1==t_first)
            p0 = np.array([constants.det_X[firstDet], constants.det_Y[firstDet], 0])
##            print(firstDet)
            detPoints = []                  ## detectors with next hits
            p = np.zeros((3,3)) 
            for i in range(4):
                if t[i] >= t_first:
                    if t[i]>t_first:
                      detPoints.append(i)
                    t[i] -= t_first
##            print(detPoints)
            for i in range(len(detPoints)):
              n = detPoints[i]
              p[i][:] = getPoint(n)
##              print(p[i])          
            v1 = p[1] - p0              ## shiiiit
            v2 = p[2] - p0
            v3 = p[3] - p0
            cp1 = np.cross(v1,v2)
            cp2 = np.cross(v1,v3)
            cp3 = np.cross(v2,v3)
            vector = cp1+cp2+cp3
            return vector
##-----------------------------------------
##-----------------------------------------
def read():
    readout.readLoop()

def ana1():
    lines = readout.getEvents()
    for i in range(len(lines)):
        evt = Event(lines[i])

    
def main():
    thread1 = threading.Thread(target = read())                 ## that will most probably not work, just trying
    thread2 = threading.Thread(target = ana1(), args = (lines))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    print('skipping the *main.py* for now')
    main()
