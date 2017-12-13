'''
FUW_cosmic_shower
    main.py
deals with multiple threads
'''


import readout
import analize
import threading
import time

print("START")
Analize = analize.Analize()
print("Constructor")


threadLoop = threading.Thread(target = Analize.anaLoop)
threadHourFlux = threading.Thread(target = Analize.GetHourFlux)
threadTotalFlux = threading.Thread(target = Analize.GetTotalFlux)
print("Thread init")
threadLoop.start()
threadHourFlux.start()
threadTotalFlux.start()
print("Threads started")


        
