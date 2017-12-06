import constants 
import readout
import event
import numpy as np
import math as math
import threading
import time

class Analize():

    def __init__(self):
        self.detectedMuons = 0
        self.flux_per_min = []
        self.muonsInMin = 0
        self.ReadOut = readout.ReadOut()
        self.thread = threading.Thread(target = self.ReadOut.readLoop)
        self.thread.start()
        self.constants = constants.Constants()
    
    def anaLoop(self):
        while(1):
            lines = self.ReadOut.getEvents()
            for i in range(len(lines)):
##                print(lines[i])
                evt = event.Event(lines[i])
##                print(evt.nMuons)
                if evt.vector is not None: print(evt.vector)
                self.detectedMuons += evt.nMuons
##                if np.sum(evt.vector) != 0: print(evt.vector)
##                time.sleep(1) #do not use sleep if no necessary
            
    def GetHourFlux(self):
        time.sleep(50) #FIXME to tak nie moze byc, bo program tu sie zatrzymuje na 598 s i spi :)
        print("Flux (per cm^2, per second) for every 1 minute in last hour: {}".format(self.flux_hour))
        return self.flux_hour

    def GetTotalFlux(self):
##        print("Total number of detected muons: {}".format(self.detectedMuons))
##        print("Total time of experiment: {}".format(time.time() - self.time0))
        return self.detectedMuons/(self.constants.det_area*(time.time() - self.ReadOut.time0)*self.constants.det_eff*self.constants.readOut_eff) #change of elapsed time
        
