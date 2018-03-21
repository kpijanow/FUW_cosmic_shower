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
from queue import Queue
from threading import Lock


class Analize():

    def __init__(self):
        self.detectedMuons = 0
        self.flux_per_min = np.zeros(120)
        self.zenith_histo = np.zeros(7)
        self.zenith_histo1 = np.zeros(7)
        self.muonsInMin = 0
        self.time = 0
        self.ReadOut = readout.ReadOut()
        self.thread = threading.Thread(target = self.ReadOut.readLoop)
        self.thread.start()
        self.constants = constants.Constants()
        self.newMinute = False
        self.flux_hour = []
        self.minutes = 0
        self.lastVector = [0,0,0]
        self.lastDetectors = [0,0,0,0]
        self.lastArrivalTimes = [0,0,0,0]
        self.showers = [0, 0, 0, 0]
        self.whichCoinc = [0, 0, 0, 0, 0, 0]
        self.zenithbins = [0, 10, 20, 30, 40, 60, 80, 100]
        self.rad_histo = np.zeros(6)
        self.rad_bins = [0, 2, 3, 4, 5, 6, 9]
        self.det_histo = np.zeros(4)
        self.evt = 0
        
        self.q = Queue(maxsize = 7)
        
        self.timeInterv = 720 #sec
        self.timeBin = 120
##        self.mutex = Lock()
    
    def anaLoop(self):
##        self.mutex.acquire()        #lock begin
        self.q.put_nowait(self.flux_per_min)
        self.q.task_done()
        self.q.put_nowait(self.TotalFlux())
        self.q.task_done()
        self.q.put_nowait(self.zenith_histo)
        self.q.task_done()
        self.q.put_nowait(self.rad_histo)
        self.q.task_done()
        self.q.put_nowait(self.lastDetectors)
        self.q.task_done()
        self.q.put_nowait(self.lastVector)
        self.q.task_done()
        self.q.put_nowait(self.lastArrivalTimes)
        self.q.task_done()
##        self.mutex.release()        #lock end
        
        while(1):
            try:
                lines = self.ReadOut.getEvents()
                
                for i in range(len(lines)):
                    self.evt = event.Event(lines[i])                
                    self.time = self.evt.time
                    self.newMinute = self.NewMinute()
                    self.DetectorsFired()
                    self.detectedMuons += self.evt.nMuons
                    self.UpdateFlux()
                            
                    if self.evt.vector is None:
                        continue
                    
                    self.ShowerRadius()
                    self.ZenithAngle()
                    self.showers[self.evt.nMuons - 1] += 1
                    self.DetectorCoincidence()
                    print(str(self.evt.vector) + " coincidence = " + str(self.evt.nMuons) + " " + str(self.whichCoinc))
                    
                    self.lastVector = self.evt.vector
                    self.lastDetectors = self.evt.detectorsFired
                    self.lastArrivalTimes = self.evt.arrivalTimes
                    sys.stdout.flush()

                time.sleep(0.5)

    ##            self.mutex.acquire()        #Lock begin
                if self.q.full() == True:
                    self.q.get_nowait()
                    self.q.get_nowait()
                    self.q.get_nowait()
                    self.q.get_nowait()
                    self.q.get_nowait()
                    self.q.get_nowait()
                    self.q.get_nowait()
                    
                self.q.put_nowait(self.flux_per_min)
                self.q.task_done()
                self.q.put_nowait(self.TotalFlux())
                self.q.task_done()
                self.q.put_nowait(self.zenith_histo)
                self.q.task_done()
                self.q.put_nowait(self.rad_histo)
                self.q.task_done()
                self.q.put_nowait(self.lastDetectors)
                self.q.task_done()
                self.q.put_nowait(self.lastVector)
                self.q.task_done()
                self.q.put_nowait(self.lastArrivalTimes)
                self.q.task_done()
    ##            self.mutex.release()        #Lock end
            except Exception as e:
                with open("error.txt", "a") as errFile:
                    errFile.write(e)
        
    def DetectorsFired(self):
        #histograms of detectors fired
        for i in range(4):
            if self.evt.detectorsFired[i]:
                self.det_histo[i] += 1
    
    def ShowerRadius(self):
        #histogram of shower radius
        for i in range(1,7):
            if self.evt.radius > self.rad_bins[i-1] and self.evt.radius<=self.rad_bins[i]:
                self.rad_histo[i-1] += 1
                
    def ZenithAngle(self):
        #histogram of zenith angle
        if self.evt.vector[2] != 0:
            if self.evt.vector[0] != 0 and self.evt.vector[0] != 1:
                index = self.evt.zenith
##                print("ZENITYHHHHHHH :" + str(self.evt.zenith))
##                print(str(int(math.atan(math.sqrt(self.evt.vector[0] * self.evt.vector[0] + self.evt.vector[1] * self.evt.vector[1])/self.evt.vector[2])/3.14*180)))
##                index = math.atan(math.sqrt(self.evt.vector[0] * self.evt.vector[0] + self.evt.vector[1] * self.evt.vector[1])/self.evt.vector[2])/3.14*180
                for i in range(1,8):
                    if index >= self.zenithbins[i-1] and index < self.zenithbins[i]:
                        self.zenith_histo[i-1] += 1
                        self.zenith_histo1[i-1] += 1
            elif self.evt.vector[0] == 0:
                self.zenith_histo[0] += 1
                self.zenith_histo1[0] += 1
            else:
                self.zenith_histo1[0] += 1

                   
    def DetectorCoincidence(self):      
        #histogram of detectors coincidence
        if(self.evt.nMuons == 2):
            if(self.evt.detectorsFired[0] == 1 and self.evt.detectorsFired[1] == 1): self.whichCoinc[0] += 1
            elif(self.evt.detectorsFired[0] == 1 and self.evt.detectorsFired[2] == 1): self.whichCoinc[1] += 1
            elif(self.evt.detectorsFired[0] == 1 and self.evt.detectorsFired[3] == 1): self.whichCoinc[2] += 1
            elif(self.evt.detectorsFired[1] == 1 and self.evt.detectorsFired[2] == 1): self.whichCoinc[3] += 1
            elif(self.evt.detectorsFired[1] == 1 and self.evt.detectorsFired[3] == 1): self.whichCoinc[4] += 1
            elif(self.evt.detectorsFired[2] == 1 and self.evt.detectorsFired[3] == 1): self.whichCoinc[5] += 1
                    
    def NewMinute(self):
        if int(self.time / self.timeInterv) != self.minutes and self.newMinute == False:
            self.minutes = int(self.time / self.timeInterv)
            return True 
        else:
            return self.newMinute
                
    def UpdateFlux(self):
        self.muonsInMin += self.evt.nMuons
        if self.newMinute:
            self.flux_per_min = np.append(self.flux_per_min, self.muonsInMin/(4*self.constants.det_area*10000*(self.timeInterv/60)*self.constants.det_eff*self.constants.readOut_eff))
            self.flux_per_min = self.flux_per_min[1:self.timeBin + 2]
            self.muonsInMin = 0
            self.newMinute = False
               
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
        print("h" + str(self.HourFlux()))
        print("zenith" + str(self.zenith_histo))
        print("zenith ++" + str(self.zenith_histo1))
        print("showers" + str(self.showers))
        print("det hits" + str(self.det_histo))
        print("radius" + str(self.rad_histo))
        print("t" + str(self.TotalFlux()))
        print(time.ctime())
        threading.Timer(3600, self.PrintZenith).start()

    def PrintTotalFlux(self):
        # every hour update the total detected flux
        print("t" + str(self.TotalFlux()))
        print(time.ctime())
        threading.Timer(3600, self.PrintTotalFlux).start()
    
