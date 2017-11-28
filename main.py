import readout
import analize
import threading
import time

print("START")
ReadOut = readout.ReadOut()
print("Constructor")

thread1 = threading.Thread(target = ReadOut.readLoop)
##thread2 = threading.Thread(target = Analize.anaLoop)
print("Thread init")
thread1.start()
##thread2.start()
print("Thread start")
#thread1.join()
#thread2.join()
#print("Thread join")

while 1:
    print("while")
    lines = ReadOut.getEvents()
    for i in range(len(lines)):
        print(lines[i])
        evt = Analize.Event(lines[i])
    time.sleep(1)
        
