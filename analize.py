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


import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from win_try import *
from queue import Queue
from matplotlib.figure import Figure

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
        self.evt = 0
        
        self.q = Queue(maxsize = 3)
    
    def anaLoop(self):
        while(1):
            lines = self.ReadOut.getEvents()
            print("while + 1")
            for i in range(len(lines)):
                self.evt = event.Event(lines[i])                
                self.time = self.evt.time
                print("time = " + str(time.time()) + "timeEv = " + str(self.time) + " minutes = " + str(self.minutes))
                self.newMinute = self.NewMinute()
                self.DetectorsFired()
                self.detectedMuons += self.evt.nMuons
                self.UpdateFlux()
                
                sys.stdout.flush()
                        
                if self.evt.vector is None:
                    continue
                
                self.ShowerRadious()
                self.ZenithAngle()
                self.showers[self.evt.nMuons - 1] += 1
                self.DetectorCoincidence()
                print(str(self.evt.vector) + " coincidence = " + str(self.evt.nMuons) + " " + str(self.whichCoinc))
                self.q.put(self.flux_per_min)
                print(self.flux_per_min)
                self.q.put(self.TotalFlux())
                self.q.put(self.zenith_histo)
                self.lastVector = self.evt.vector
                self.lastDetectors = self.evt.detectorsFired
                
            time.sleep(0.2)
            
            
    def InitializeWindow(self):
        app = tk.Tk()
        f2 = plt.figure()
        gs = gridspec.GridSpec(3,3)
        a = f2.add_subplot(gs[0,:-1])
        a_txt = f2.add_subplot(gs[0,-1])
        a_sh = f2.add_subplot(gs[1:,:-1], projection='3d')
        ax_h = f2.add_subplot(gs[-1, -1])
        #plt.ion()
        
        canvas = FigureCanvasTkAgg(f2, master = app)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, app)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)   
        ani = animation.FuncAnimation(f2, animate, fargs = [self.q, a, a_txt, ax_h, ], interval = 10000)
        #ani2 = animation.FuncAnimation(f2, animate_his, fargs = [recentZenithHisto, ax_h], interval=1000)
        #ani3 = animation.FuncAnimation(f2, ani_shower, fargs = [Analize.lastVector, recentShowerDetectors, a_sh])
        ##ani4 = animation.FuncAnimation(f2, flux_text, fargs = [q, a_txt], interval=1000)
        
        plt.draw()
        print("plt.draw()")
        app.mainloop()
        print("app.mainloop()")
        
    def DetectorsFired(self):
        #histograms of detectors fired
        for i in range(4):
            if self.evt.detectorsFired[i]:
                self.det_histo[i] += 1
    
    def ShowerRadious(self):
        #histogram of shower radious
        for i in range(1,7):
            if self.evt.radius > self.rad_bins[i-1] and self.evt.radius<=self.rad_bins[i]:
                self.rad_histo[i-1] += 1
                
    def ZenithAngle(self):
        #histogram of zenith angle
        if self.evt.vector[2] != 0:
            if self.evt.vector[0] != 0 and self.evt.vector[1] != 0:
                index = int(math.atan(math.sqrt(self.evt.vector[0] * self.evt.vector[0] + self.evt.vector[1] * self.evt.vector[1])/self.evt.vector[2])/3.14*180*20/90)
                for i in range(1,8):
                    if index >= self.zenithbins[i-1] and index < self.zenithbins[i]:    self.zenith_histo[i-1] += 1
            else:
                self.zenith_histo[0] += 1
        ##                            print ("else")
                   
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
        if int(self.time / 60) != self.minutes and self.newMinute == False:
            self.minutes = int(self.time / 60)
            return True 
        else:
            return self.newMinute


    
##    def NewHour(self):
##        if self.time % 3600:  return True  
##        else:               return False
                
    def UpdateFlux(self):
        self.muonsInMin += self.evt.nMuons
        print(self.muonsInMin)
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
        print("zenith" + str(self.zenith_histo))
        print("showers" + str(self.showers))
        print("det hits" + str(self.det_histo))
        print("radius" + str(self.rad_histo))
        print("t" + str(self.TotalFlux()))
        threading.Timer(60, self.PrintHourFlux).start()

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
    
