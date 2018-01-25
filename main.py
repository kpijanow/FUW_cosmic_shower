'''
FUW_cosmic_shower
    main.py
deals with multiple threads
'''


import readout
import analize
import threading
import time
import numpy as np

from win_try import *

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
tableOfFluxInEveryMinute = Analize.flux_per_min #flux (not adapted)
print(tableOfFluxInEveryMinute)
totalFlux = Analize.TotalFlux() #txt
print(totalFlux)
recentShowerVector = Analize.lastVector #vec_t
print(recentShowerVector)
recentShowerDetectors = Analize.lastDetectors #vec_d
print(recentShowerDetectors)
recentZenithHisto = Analize.zenith_histo
print(type(recentZenithHisto))

#gui test
totalFlux = str(901.8)
tableOfFluxInEveryMinute = np.zeros(60)+2
recentShowerDetectors = np.array([1,1,1,1])
recentShowerVector = np.array([ 0.02, -0.03, 0.98])
recentZenithHisto = np.zeros(20)+1

#0, 90, 20 bin, 
print(recentZenithHisto)
print("GUI test")


f2 = plt.figure()
gs = gridspec.GridSpec(3,3)
a = f2.add_subplot(gs[0,:-1])
a_txt = f2.add_subplot(gs[0,-1])
a_sh = f2.add_subplot(gs[1:,:-1], projection='3d')
ax_h = f2.add_subplot(gs[-1, -1])

ani = animation.FuncAnimation(f2, animate, fargs = [tableOfFluxInEveryMinute], interval=5000)
ani2 = animation.FuncAnimation(f2, animate_his, fargs = [recentZenithHisto, ax_h], interval=1000)
ani3 = animation.FuncAnimation(f2, ani_shower, fargs = [recentShowerVector, recentShowerDetectors, a_sh], interval=50)#ani = animation.FuncAnimation(f2, animate, interval=1000)
ani4 = animation.FuncAnimation(f2, flux_text, fargs = [str(totalFlux), a_txt], interval=1000)
plt.show()
