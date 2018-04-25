import serial as serial
import binascii
import time
import glob, os
import threading
import sys

class ReadOut():
    
    def __init__(self):
        self.line = b''
        self.new = False
        self.events = list()
        self.t1 = [-5, -5, -5, -5]
        self.t2 = [-5, -5, -5, -5]
        self.time0 = time.time() #global time0
        self.timeE = 0          #global event time - global time0
        self.ser = 0
        self.lostLines = 0

    def setDAQparameters(self):
        if (self.ser.writable()):
            self.ser.write(b'WC 0 F\r\n') #send signal to DAQ to read from 4 detectors
                                          #and corelarion 1                                  
            self.ser.flush()

    
    def get2Bytes(self, n):
        try:
            return bin(int(self.line[n:n+2].decode("utf8"), 16))[2:].zfill(8)
        except:
            return 0

    def checkIfNewEvent(self):
        try:
            bits = self.get2Bytes(9)
            if bits[0] == '1':
                return True
            else:
                return False
        except:
            return True
        
    def checkIfGoodData(self, i):
        try:
            bits = self.get2Bytes(9 + i * 3)
            if bits[2] == '1':
                return True
            else:
                return False
        except:
            return False

    def getTimeTicks(self):
        for i in range(4):
            if self.checkIfGoodData(i * 2):
                bits = self.get2Bytes(9 + i * 6)
                self.t1[i] = int(bits[3:], 2)
##                print("if " + str(i) + " " + str(self.t1[i]))
            elif self.t1[i] < -1:
##                print("el " + str(i) + " " + str(self.t1[i]))
                self.t1[i] = -0.8
            
            if self.checkIfGoodData(i * 2 + 1):
                bits = self.get2Bytes(12 + i * 6)
                self.t2[i] = int(bits[3:], 2)
            elif self.t2[i] < -1:
                self.t2[i] = -0.8

    def timeTicksToNanoS(self):
        self.t1[:] = [x*5/4.0 for x in self.t1]
        self.t2[:] = [x*5/4.0 for x in self.t2]

    def checkIfGoodReadout(self):
        for i in range(4):
            if self.t1[i] >= 0:
                if (self.t2[i] >= 0) and (self.t2[i] < self.t1[i]):
                    self.t2[i] += 40

    def updateEvents(self):
        t = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        t[0:4] = self.t1
        t[4:8] = self.t2
        t[8] = self.timeE
        if (len(self.events) < 1500):
            self.events.append(t)

    def process(self):
        self.timeE = time.time() - self.time0
        self.new = True
        self.timeTicksToNanoS()
        self.checkIfGoodReadout()
        self.updateEvents()
        
        self.t1[:] = [-5 for x in self.t1]
        self.t2[:] = [-5 for x in self.t2]
        self.getTimeTicks()

    def readLine(self):
        if len(self.line) == 74:
            if self.checkIfNewEvent():
                self.process()	
            else:
                self.new = False
                self.getTimeTicks()
                
        elif len(self.line) == 142:
            line0 = self.line
            self.line = line0[0:68]
            if self.checkIfNewEvent():
                self.process()		
            else:
                self.new = False
                self.getTimeTicks()
                
            self.line = line0[68:]
            if self.checkIfNewEvent():
                self.process()		
            else:
                self.new = False
                self.getTimeTicks()
        elif len(self.line.split()) >= 9:
            if len(self.line.split()[0]) == 8 and len(self.line.split()[1]) == 2:
                if self.checkIfNewEvent():
                    self.process()	
                else:
                    self.new = False
                    self.getTimeTicks()
        elif self.line == b'0000000 000000.000 000000 V 00 8 +0000\r\n':
            return
        else:
            self.lostLines += 1
            #print("lost = " + str(self.lostLines) + " line lenghth = " + str(len(self.line)) + " line " + self.line)

    def connectToSerial(self):
        os.chdir("/dev")
        for file in glob.glob("ttyUSB*"):
            print(file)
            try:
                self.ser = serial.Serial('/dev/' + str(file), baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, xonxoff = True, timeout = 0)
                self.ser.open()
                print("connected to " + str(file))
            except:
                print(str(file) + " checked")

    def readLoop(self):
        """readout loop that should run in background"""
        self.connectToSerial()
        self.setDAQparameters()
        self.ser.flushInput()
        
        while(True):
            #self.ser.close
            try:
                #print("try " + str(self.ser.isOpen()) + "\n")
                time.sleep(0.3)
                lines = self.ser.readlines()
                
                
                #if len(lines) != 0 : print(len(lines))
            except:
                print("USB disconected :( ")
                self.ser.close()
                self.connectToSerial()
                time.sleep(1)
                lines = []

            try:
                if (len(lines) < 1500):
                    for line0 in lines:
                        self.line = line0
                        if self.line != b'':
                            self.readLine()
                else:
                    for i in range(1200):
                        self.line = lines[i]
                        if self.line != b'':
                            self.readLine()
                            
            except Exception as e:
                with open("error.txt", "a") as errFile:
                    errFile.write(e)
                    print(e.args)
                
    def getEvents(self):
        """Get recorded events and clear the list
        returns list of events with structure:
            [t1_1, t1_2, t1_3, t1_4, t2_1, t2_2, t2_3, t2_4, T]
        where: t1_x - is start of the signal in ns form the x-th detector
               t2_x - is start of the signal in ns form the x-th detector
               T    - is an absolute time of the signal in seconds form the start of the program"""
        #print("number of events taken " + str(len(self.events)))
        events0 = self.events
        self.events = []
        return events0
            
