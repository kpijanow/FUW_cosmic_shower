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
        self.time = 0
    
    def anaLoop():
        lines = readout.getEvents()
        for i in range(len(lines)):
            print(lines[i])
            evt = event.Event(lines[i])
            time.sleep(1)
            
    def GetHourFlux():
        time.sleep(598)
        print("Flux (per cm^2, per second) for every 1 minute in last hour: {}".format(self.flux_hour))
        return self.flux_hour

    def GetTotalFlux():
        print("Total number of detected muons: {}".format(self.detectedMuons))
        print("Total time of experiment: {}".format(self.time))
        return delf.detectedMuons/(constants.det_area*self.time)
        
