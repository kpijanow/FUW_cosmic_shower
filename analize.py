'''
project: FUW_cosmic_shower
    analize.py
Analyze each read event,
compute flux (per minute, total)
'''

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
        self.time = event.Event.time
        self.newMinute = self.NewMinute()
        self.newHour = self.NewHour()
    
    def anaLoop(self):
        while(1):
            lines = self.ReadOut.getEvents()
            for i in range(len(lines)):
                evt = event.Event(lines[i])
                if evt.vector is not None: print(evt.vector)
                self.detectedMuons += evt.nMuons

    def NewMinute(self):
        if self.time % 60:  return True
        else:               return False

    def NewHour(self):
        if self.time % 3600:  return True  
        else:               return False
                
    def UpdateFlux(self):
        self.muonsInMin += evt.nMuons
        if self.newMinute:
            flux_per_min.append(analize.muonsInMin/(60*self.const.det_area))
            self.muonsInMin = 0
        if self.newHour:
            self.flux_hour = self.flux_per_min
            self.flux_per_min = []
        
            
    def HourFlux(self):
        return self.flux_hour

    def TotalFlux(self):
        return self.detectedMuons/(self.constants.det_area*(event.Event.time - self.ReadOut.time0)*self.constants.det_eff*self.constants.readOut_eff) 

#------------------ 
#class independent:

def GetHourFlux():
    # every hour get list flux per min in previous hour -> then show average or whatever in a histo
    print(Ana.HourFlux())
    threading.Timer(3600, GetHourFlux).start()

def GetTotalFlux():
    # every hour update the total detected flux
    print(Ana.TotalFlux())
    threading.Timer(3600, GetTotalFlux).start()

    
