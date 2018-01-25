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
import sys

class Analize():

    def __init__(self):
        self.detectedMuons = 0
        self.flux_per_min = np.zeros(60)
        self.zenith_histo = np.zeros(20)
        self.muonsInMin = 0
        self.time = 0
        self.ReadOut = readout.ReadOut()
        self.thread = threading.Thread(target = self.ReadOut.readLoop)
        self.thread.start()
        #self.ReadOut.readLoop()
        self.constants = constants.Constants()
        self.newMinute = False
##        self.newHour = False
        self.flux_hour = []
        self.minutes = 0
        self.lastVector = [0,0,0]
        self.lastDetectors = [0,0,0,0]
    
    def anaLoop(self):
        while(1):
            lines = self.ReadOut.getEvents()
            for i in range(len(lines)):
                evt = event.Event(lines[i])
                self.time = evt.time
                self.newMinute = self.NewMinute()
##                self.newHour = self.NewHour()
                if evt.vector is not None:
                    if evt.vector[0] != 0 and evt.vector[1] != 0:
                        index = int(math.atan(math.sqrt(evt.vector[0] * evt.vector[0] + evt.vector[1] * evt.vector[1])/evt.vector[2])/3.14*180*20/90)
                        if index < 20:
                            self.zenith_histo[index] += 1
                    else:
                        self.zenith_histo[0] += 1
                    print(evt.vector)
                    self.lastVector = evt.vector
                    self.lastDetectors = evt.detectorsFired
                self.detectedMuons += evt.nMuons
                self.UpdateFlux(evt)
                sys.stdout.flush()
            time.sleep(1)
                

    def NewMinute(self):
        if int(self.time / 60) != self.minutes and self.newMinute == False:
            self.minutes = int(self.time / 60)
            return True 
        else:
            return self.newMinute

##    def NewHour(self):
##        if self.time % 3600:  return True  
##        else:               return False
                
    def UpdateFlux(self, evt):
        self.muonsInMin += evt.nMuons
        if self.newMinute:
            self.flux_per_min = np.append(self.flux_per_min, self.muonsInMin/(4*self.constants.det_area*10000*self.constants.det_eff*self.constants.readOut_eff))
            self.flux_per_min = self.flux_per_min[1:62]
            self.muonsInMin = 0
            self.newMinute = False
        #if self.newHour:
            #self.flux_hour = self.flux_per_min
            #self.flux_per_min = []
        
            
    def HourFlux(self):
        return self.flux_per_min

    def ZenithHisto(self):
        return self.zenith_histo

    def TotalFlux(self):
        if self.time != 0:
            return self.detectedMuons/(4*self.constants.det_area*10000*(self.time/60)*self.constants.det_eff*self.constants.readOut_eff)
        else:
            return 0

    def PrintHourFlux(self):
        # every hour get list flux per min in previous hour -> then show average or whatever in a histo
        print("h" + str(self.HourFlux()))
        threading.Timer(3600, self.PrintHourFlux).start()

    def PrintZenith(self):
        # every hour get list flux per min in previous hour -> then show average or whatever in a histo
        print("z" + str(self.zenith_histo))
        threading.Timer(3600, self.PrintZenith).start()

    def PrintTotalFlux(self):
        # every hour update the total detected flux
        print("t" + str(self.TotalFlux()))
        print(time.ctime())
        threading.Timer(3600, self.PrintTotalFlux).start()
    
