import serial as serial
import binascii

class ReadOut():
    
    def __init__(self):
        self.line = b''
        self.new = False
        self.events = list()
        self.t1 = [0, 0, 0, 0]
        self.t2 = [0, 0, 0, 0]
    
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
            else:
                self.t1[i] = -1
            
            if self.checkIfGoodData(self.line, i * 2 + 1):
                bits = self.get2Bytes(12 + i * 6)
                self.t2[i] = int(bits[3:], 2)
            else:
                self.t1[i] = -1

    def timeTicksToNanoS(self):
        self.t1[:] = [x*5/4.0 for x in self.t1]
        self.t2[:] = [x*5/4.0 for x in self.t2]

    def checkIfGoodReadout(self):
        for i in range(4):
            if self.t1[i] >= 0:
                if (self.t2[i] >= 0) and (self.t2[i] < self.t1[i]):
                    self.t2[i] += 40

    def updateEvents(self):
        t = [0, 0, 0, 0, 0, 0, 0, 0]
        t[1:5] = self.t1
        t[4:] = self.t2
        self.events.append(t)

    def readLine(self):
        if len(self.line) == 74:
            if self.checkIfNewEvent():
                self.new = True
                self.timeTicksToNanoS()
                self.checkIfGoodReadout()
                self.updateEvents()
        
                self.t1[:] = [0 for x in self.t1]
                self.t2[:] = [0 for x in self.t2]
                self.getTimeTicks(self.line)
		
            else:
                self.getTimeTicks(self.line)

    def readLoop(self):
        ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, xonxoff = True, timeout = 0)
        while 1:
            ser.close
            self.line = ser.readline()
            if self.line != b'':
                self.readLine()
            
    def getEvents(self):
        events0 = self.events
        self.events = []
        return events0
            
