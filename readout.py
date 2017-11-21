import serial as serial
import binascii

class ReadOut():
    line = b''
    new = False
    events = list()
    
    def get2Bytes(n):
        global line
	return bin(int(line[n:n+2].decode("utf8"), 16))[2:].zfill(8)

    def checkIfNewEvent():
	bits = get2Bytes(9)
	if bits[0] == '1':
	    return True
	else:
	    return False

    def checkIfGoodData(i):
	bits = get2Bytes(9 + i * 3)
	if bits[2] == '1':
	    return True
	else:
	    return False

    def getTimeTicks():
        global line
	for i in range(4):
	    if checkIfGoodData(i * 2):
		bits = get2Bytes(9 + i * 6)
		t1[i] = int(bits[3:], 2)
	    else:
                t1[i] = -1
                
            if checkIfGoodData(line, i * 2 + 1):
		bits = get2Bytes(12 + i * 6)
		t2[i] = int(bits[3:], 2)
	    else:
                t1[i] = -1

    def timeTicksToNanoS():
	self.t1[:] = [x*5/4.0 for x in self.t1]
	self.t2[:] = [x*5/4.0 for x in self.t2]

    def checkIfGoodReadout():
	for i in range(4):
            if t1[i] >= 0:
		if (t2[i] >= 0) and (t2[i] < t1[i]):
                    t2[i] += 40

    def updateEvents():
        t = [0, 0, 0, 0, 0, 0, 0, 0]
        t[1:5] = self.t1
        t[4:] = self.t2
        self.events.append(t)

    def readLine(line):
        ser.close
        line = ser.readline()
        if line != b'':
        readLine(line)
	
	if len(line) == 74:
	    if checkIfNewEvent(line):
                self.new = True
		timeTicksToNanoS()
		checkIfGoodReadout()
		updateEvents()
					
		self.t1[:] = [0 for x in t1]
		self.t2[:] = [0 for x in t2]
		getTimeTicks(line)
		
            else:
                getTimeTicks(line)

    def readLoop:
        ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, xonxoff = True, timeout = 0)
        while 1:
            ser.close
            line = ser.readline()
            if line != b'':
                readLine(line)
            
    def getEvents():
        events0 = events
        events = []
        return events0
            
