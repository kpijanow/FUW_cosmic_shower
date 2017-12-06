import serial as serial
import binascii
import time

class ReadOut():
    
    def __init__(self):
        self.line = b''
        self.new = False
        self.events = list()
        self.t1 = [-5, -5, -5, -5]
        self.t2 = [-5, -5, -5, -5]
        self.time0 = time.time() #global time0
        self.timeE = 0          #global event time - global time0
    
    def get2Bytes(self, n):
        return bin(int(self.line[n:n+2].decode("utf8"), 16))[2:].zfill(8)

    def checkIfNewEvent(self):
        bits = self.get2Bytes(9)
        if bits[0] == '1':
            return True
        else:
            return False

    def checkIfGoodData(self, i):
        bits = self.get2Bytes(9 + i * 3)
        if bits[2] == '1':
            return True
        else:
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
        self.events.append(t)

    def readLine(self):
        if len(self.line) == 74:
            if self.checkIfNewEvent():
                self.timeE = time.time() - self.time0
                self.new = True
                self.timeTicksToNanoS()
                self.checkIfGoodReadout()
                self.updateEvents()
        
                self.t1[:] = [-5 for x in self.t1]
                self.t2[:] = [-5 for x in self.t2]
                self.getTimeTicks()
		
            else:
                self.new = False
                self.getTimeTicks()

    def readLoop(self):
        """readout loop that should run in background"""
        
        ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, xonxoff = True, timeout = 0)
        while 1:
            ser.close
            self.line = ser.readline()
            if self.line != b'':
                self.readLine()
            
    def getEvents(self):
        """Get recorded events and clear the list
        returns list of events with structure:
            [t1_1, t1_2, t1_3, t1_4, t2_1, t2_2, t2_3, t2_4, T]
        where: t1_x - is start of the signal in ns form the x-th detector
               t2_x - is start of the signal in ns form the x-th detector
               T    - is an absolute time of the signal in seconds form the start of the program"""
        events0 = self.events
        self.events = []
        return events0
            
