import readout
import threading
import time

print("START")
ReadOut = readout.ReadOut()
print("Constructor")

thread1 = threading.Thread(target = ReadOut.readLoop)
print("Thread init")
thread1.start()
print("Thread start")
#thread1.join()
#print("Thread join")

while 1:
    print("while")
    lines = ReadOut.getEvents()
    for i in range(len(lines)):
        print(lines[i])
    time.sleep(1)
        
