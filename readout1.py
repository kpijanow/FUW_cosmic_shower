import serial as serial
import binascii
import time
import glob, os
import threading

class ReadOutEventC():
    def __init__(self, line0):
        self.line = line0 #b''
        self.new = False
        self.events = list()
        self.t1 = [-5, -5, -5, -5]
        self.t2 = [-5, -5, -5, -5]
        self.time0 = time.time() #global time0
        self.timeE = 0          #global event time - global time0
        
class ReadOut():
    
    def __init__(self):
        self.line = b''
        self.new = False
        self.events = list()
        self.t1 = [-5, -5, -5, -5]
        self.t2 = [-5, -5, -5, -5]
        self.time0 = time.time() #global time0
        self.timeE = 0          #global event time - global time0

    def setDAQparameters(self):
        if (self.ser.writable()):
            self.ser.write(b'WC 0 F\r\n') #send signal to DAQ to read from 4 detectors
                                          #and corelarion 1                                  
            self.ser.flush()

    
    def get2Bytes(self, n, ReadOutEvent):
        return bin(int(ReadOutEvent.line[n:n+2].decode("utf8"), 16))[2:].zfill(8)

    def checkIfNewEvent(self, ReadOutEvent):
        bits = self.get2Bytes(9, ReadOutEvent)
        if bits[0] == '1':
            return True
        else:
            return False

    def checkIfGoodData(self, i, ReadOutEvent):
        bits = self.get2Bytes(9 + i * 3, ReadOutEvent)
        if bits[2] == '1':
            return True
        else:
            return False

    def getTimeTicks(self, ReadOutEvent):
        for i in range(4):
            if self.checkIfGoodData(i * 2, ReadOutEvent):
                bits = self.get2Bytes(9 + i * 6, ReadOutEvent)
                ReadOutEvent.t1[i] = int(bits[3:], 2)
##                print("if " + str(i) + " " + str(self.t1[i]))
            elif ReadOutEvent.t1[i] < -1:
##                print("el " + str(i) + " " + str(self.t1[i]))
                ReadOutEvent.t1[i] = -0.8
            
            if self.checkIfGoodData(i * 2 + 1, ReadOutEvent):
                bits = self.get2Bytes(12 + i * 6, ReadOutEvent)
                ReadOutEvent.t2[i] = int(bits[3:], 2)
            elif ReadOutEvent.t2[i] < -1:
                ReadOutEvent.t2[i] = -0.8

    def timeTicksToNanoS(self, ReadOutEvent):
        ReadOutEvent.t1[:] = [x*5/4.0 for x in ReadOutEvent.t1]
        ReadOutEvent.t2[:] = [x*5/4.0 for x in ReadOutEvent.t2]

    def checkIfGoodReadout(self, ReadOutEvent):
        for i in range(4):
            if ReadOutEvent.t1[i] >= 0:
                if (ReadOutEvent.t2[i] >= 0) and (ReadOutEvent.t2[i] < ReadOutEvent.t1[i]):
                    ReadOutEvent.t2[i] += 40

    def updateEvents(self, ReadOutEvent):
        t = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        t[0:4] = ReadOutEvent.t1
        print(t[0:4])
        t[4:8] = ReadOutEvent.t2
        t[8] = ReadOutEvent.timeE
        self.events.append(t)

    def process(self, ReadOutEvent):
        ReadOutEvent.timeE = time.time() - ReadOutEvent.time0
        self.new = True
        self.timeTicksToNanoS(ReadOutEvent)
        self.checkIfGoodReadout(ReadOutEvent)
        self.updateEvents(ReadOutEvent)
        
        self.t1[:] = [-5 for x in self.t1]
        self.t2[:] = [-5 for x in self.t2]
        self.getTimeTicks(ReadOutEvent)

    def readLine(self, ReadOutEvent):
        if len(ReadOutEvent.line) == 74:
            print(ReadOutEvent.line)
            if self.checkIfNewEvent(ReadOutEvent):
                self.process(ReadOutEvent)	
            else:
                self.new = False
                self.getTimeTicks(ReadOutEvent)
                
        elif len(ReadOutEvent.line) == 142:
            line0 = ReadOutEvent.line
            ReadOutEvent.line = line0[0:68]
            if self.checkIfNewEvent(ReadOutEvent):
                self.process(ReadOutEvent)		
            else:
                self.new = False
                self.getTimeTicks(ReadOutEvent)
                
            ReadOutEvent.line = line0[68:]
            if self.checkIfNewEvent(ReadOutEvent):
                self.process(ReadOutEvent)		
            else:
                self.new = False
                self.getTimeTicks(ReadOutEvent)
        else:
            print("line lenghth = " + str(len(self.line)) + " line " + self.line)

    def connectToSerial(self):
        os.chdir("/dev")
        for file in glob.glob("ttyUSB*"):
            print(file)
            try:
                self.ser = serial.Serial('/dev/' + str(file), baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, xonxoff = True, timeout = 0)
                print("connected to " + str(file))
            except:
                print(str(file) + " checked")

    def readLoop(self):
        """readout loop that should run in background"""
        self.connectToSerial()
        self.setDAQparameters()
        
        while 1:
            self.ser.close
            line0 = b''
            try:
                #lines = self.ser.readlines()
                #for line0 in lines:
                    #self.line = line0
                line0 = self.ser.readline()
            except:
                print("USB disconected :( ")
                self.connectToSerial()
                time.sleep(5)
                
            ReadOutEvent = ReadOutEventC(line0)
            if line0 != b'':
                #print("thread")
                self.thread = threading.Thread(target = self.readLine, args = (ReadOutEvent,))
                self.thread.start()
##                self.line = self.ser.readline()
##                if self.line != b'':
##                    self.readLine()
                
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
            
##class ReadOut00():
##    def __init__(self):
##        self.line = b''
##        self.ser = 0
##        
##    def connectToSerial(self):
##        os.chdir("/dev")
##        for file in glob.glob("ttyUSB*"):
##            print(file)
##            try:
##                self.ser = serial.Serial('/dev/' + str(file), baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, xonxoff = True, timeout = 0)
##                print("connected to " + str(file))
##            except:
##                print(str(file) + " checked")
##
##    def setDAQparameters(self):
##        if (self.ser.writable()):
##            self.ser.write(b'WC 0 F\r\n') #send signal to DAQ to read from 4 detectors
##                                          #and corelarion 1                             
##            self.ser.flush()
##            
##    def readLoop(self):
##        """readout loop that should run in background"""
##        self.connectToSerial()
##        self.setDAQparameters()
##        
##        while 1:
##            self.ser.close
##            try:
##                #lines = self.ser.readlines()
##                #for line0 in lines:
##                    #self.line = line0
##                line0 = self.ser.readline()
##                if line0 != b'':
##                    ReadLine = ReadLine(line0)
##                    self.thread = threading.Thread(target = ReadLine.readLine, args = line0)
##                    self.thread.start()
####                self.line = self.ser.readline()
####                if self.line != b'':
####                    self.readLine()
##            except:
##                print("USB disconected :( ")
##                self.connectToSerial()
##                time.sleep(5)       
