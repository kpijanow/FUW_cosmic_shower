import readout
import analize
import threading
import time

print("START")
#ReadOut = readout.ReadOut()
Analize = analize.Analize()
print("Constructor")

#thread1 = threading.Thread(target = ReadOut.readLoop)
thread2 = threading.Thread(target = Analize.anaLoop)
thread3 = threading.Thread(target = Analize.GetHourFlux)
print("Thread init")
thread3.start()
thread2.start()
print("Thread start")
#thread1.join()
#thread2.join()
print("Thread join")

i = 0

while 1:
    i += 1
##    print("while")
    #lines = ReadOut.getEvents()
    hour_flux = Analize.GetTotalFlux()
##    for i in range(len(lines)):
##        print(lines[i])
##        evt = Analize.Event(lines[i])
    time.sleep(1)
        
