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
        self.flux_per_min = np.ones(60)
        self.muonsInMin = 0
        self.time = 0
        self.ReadOut = readout.ReadOut()
        self.thread = threading.Thread(target = self.ReadOut.readLoop)
        self.thread.start()
        self.constants = constants.Constants()
        self.newMinute = False
        self.newHour = False
        self.flux_hour = []
        self.minutes = 0
    
    def anaLoop(self):
        while(1):
            lines = self.ReadOut.getEvents()
            for i in range(len(lines)):
                evt = event.Event(lines[i])
                self.time = evt.time
                self.newMinute = self.NewMinute()
                self.newHour = self.NewHour()
                if evt.vector is not None: print(evt.vector)
                self.detectedMuons += evt.nMuons
                self.UpdateFlux(evt)
                

    def NewMinute(self):
        if int(self.time / 60) != self.minutes and self.newMinute == False:
            self.minutes = int(self.time / 60)
            return True 
        else:
            return self.newMinute

    def NewHour(self):
        if self.time % 3600:  return True  
        else:               return False
                
    def UpdateFlux(self, evt):
        self.muonsInMin += evt.nMuons
        if self.newMinute:
            self.flux_per_min = np.append(self.flux_per_min, self.muonsInMin/(60*self.constants.det_area*self.constants.det_eff*self.constants.readOut_eff))
            self.flux_per_min = self.flux_per_min[1:62]
            self.muonsInMin = 0
            self.newMinute = False
        #if self.newHour:
            #self.flux_hour = self.flux_per_min
            #self.flux_per_min = []
        
            
    def HourFlux(self):
        return self.flux_per_min

    def TotalFlux(self):
        if self.time != 0:
            return self.detectedMuons/(self.constants.det_area*(self.time)*self.constants.det_eff*self.constants.readOut_eff)
        else:
            return 0

    def GetHourFlux(self):
        # every hour get list flux per min in previous hour -> then show average or whatever in a histo
        print("h" + str(self.HourFlux()))
        threading.Timer(3600, self.GetHourFlux).start()

    def GetTotalFlux(self):
        # every hour update the total detected flux
        print("t" + str(self.TotalFlux()))
        threading.Timer(3600, self.GetTotalFlux).start()
        
#------------------ 
#class independent:


    
