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
threadHourFlux = threading.Thread(target = Analize.PrintHourFlux)
threadTotalFlux = threading.Thread(target = Analize.PrintTotalFlux)
threadZenith = threading.Thread(target = Analize.PrintZenith)
print("Thread init")
threadHourFlux.start()
threadTotalFlux.start()
threadZenith.start()
threadLoop.start()
print("Threads started")

#data needed for gui
tableOfFluxInEveryMinute = Analize.flux_per_min
totalFlux = Analize.TotalFlux()
recentShowerVector = Analize.lastVector
recentShowerDetectors = Analize.lastDetectors
