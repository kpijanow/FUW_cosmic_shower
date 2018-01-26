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
        self.zenith_histo = np.zeros(7)
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
        self.showers = [0, 0, 0, 0]
        self.whichCoinc = [0, 0, 0, 0, 0, 0]
        self.zenithbins = [0, 10, 20, 30, 40, 60, 80, 100]
        self.rad_histo = np.zeros(6)
        self.rad_bins = [0, 2, 3, 4, 5, 6, 9]
        self.det_histo = np.zeros(4)
    
    def anaLoop(self):
        while(1):
            lines = self.ReadOut.getEvents()
            for i in range(len(lines)):
                evt = event.Event(lines[i])
                #print("TEST")
                
                self.time = evt.time
                self.newMinute = self.NewMinute()
##                self.newHour = self.NewHour()
                for i in range(4):
                    if evt.detectorsFired[i]:
                        self.det_histo[i] += 1
                if evt.vector is not None:
                    for i in range(1,7):
                        if evt.radius > self.rad_bins[i-1] and evt.radius<=self.rad_bins[i]:
                            self.rad_histo[i-1] += 1
                    if evt.vector[2] != 0:
                        if evt.vector[0] != 0 and evt.vector[1] != 0:
                            index = int(math.atan(math.sqrt(evt.vector[0] * evt.vector[0] + evt.vector[1] * evt.vector[1])/evt.vector[2])/3.14*180*20/90)
                            for i in range(1,8):
                                if index >= self.zenithbins[i-1] and index < self.zenithbins[i]:    self.zenith_histo[i-1] += 1
                        else:
                            self.zenith_histo[0] += 1
##                            print ("else")
                    
                    #print(str(evt.vector) + " coincidence = " + str(evt.nMuons))
                    self.lastVector = evt.vector
                    self.lastDetectors = evt.detectorsFired
                    self.showers[evt.nMuons - 1] += 1
                    if(evt.nMuons == 2):
                        if(evt.detectorsFired[0] == 1 and evt.detectorsFired[1] == 1): self.whichCoinc[0] += 1
                        elif(evt.detectorsFired[0] == 1 and evt.detectorsFired[2] == 1): self.whichCoinc[1] += 1
                        elif(evt.detectorsFired[0] == 1 and evt.detectorsFired[3] == 1): self.whichCoinc[2] += 1
                        elif(evt.detectorsFired[1] == 1 and evt.detectorsFired[2] == 1): self.whichCoinc[3] += 1
                        elif(evt.detectorsFired[1] == 1 and evt.detectorsFired[3] == 1): self.whichCoinc[4] += 1
                        elif(evt.detectorsFired[2] == 1 and evt.detectorsFired[3] == 1): self.whichCoinc[5] += 1
                    print(str(evt.vector) + " coincidence = " + str(evt.nMuons) + " " + str(self.whichCoinc))

                self.detectedMuons += evt.nMuons
                self.UpdateFlux(evt)
                sys.stdout.flush()
            time.sleep(0.2)
                

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
        x = self.flux_per_min
        return x

    def ZenithHisto(self):
        return self.zenith_histo
        
    def RadiusHisto(self):
        return self.rad_histo
    
    def DetHitHisto(self):
        return self.det_histo

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
        print("zenith" + str(self.zenith_histo))
        print("showers" + str(self.showers))
        print("det hits" + str(self.det_histo))
        print("radius" + str(self.rad_histo))
        threading.Timer(3600, self.PrintZenith).start()

    def PrintTotalFlux(self):
        # every hour update the total detected flux
        print("t" + str(self.TotalFlux()))
        print(time.ctime())
        threading.Timer(3600, self.PrintTotalFlux).start()
    
