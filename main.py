'''
FUW_cosmic_shower
    main.py
deals with multiple threads
'''

import analize
import threading
import time
import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from win_try import *
from queue import Queue
from matplotlib.figure import Figure

Analize = analize.Analize()
threadLoop = threading.Thread(target = Analize.anaLoop)
threadLoop.start()
print("loop started")
threadLoop = threading.Thread(target = Analize.PrintHourFlux)
threadLoop.start()
print("print started")
time.sleep(5)
Analize.InitializeWindow()
print("window initialized")

#time.sleep(1)
#
#
#q = Queue()
#q_min = Queue(maxsize = 3)
#
#def TFin(out_q):
#    while True:
#        time.sleep(1)
#
#        out_q.put(Analize.TotalFlux())
#
###threadTF = threading.Thread(target = TFin, args =(q,))
###threadTF.start()
#
#
#
#def TFMinIn(out_q):
#    while True:
#        time.sleep(1)
#        #print(Analize.flux_per_min)
#        print("works...")
#        
#        print(out_q.qsize())
###        with out_q.mutex:
###            out_q.queue.clear()
###        with out_q2.mutex:
###            out_q2.queue.clear()
#        out_q.put(Analize.HourFlux())
#        out_q.put(Analize.TotalFlux())
#        out_q.put(Analize.ZenithHisto())
#        print(threadLoop.isAlive())
#
#threadTFMin = threading.Thread(target = TFMinIn, args =(q_min, ))
#threadTFMin.start() 
#
##plt.ion()
#
##time.sleep(1)
#
#
#
#
#
##box = tk.Entry(app)
##button = tk.Button(app, text="check", command=self.plot)
##fr = tk.Frame()
#app = tk.Tk()
#f2 = plt.figure()
#gs = gridspec.GridSpec(3,3)
#a = f2.add_subplot(gs[0,:-1])
#a_txt = f2.add_subplot(gs[0,-1])
#a_sh = f2.add_subplot(gs[1:,:-1], projection='3d')
#ax_h = f2.add_subplot(gs[-1, -1])
#plt.ion()
#
#
#
#canvas = FigureCanvasTkAgg(f2, master = app)
#canvas.show()
#
#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#toolbar = NavigationToolbar2TkAgg(canvas, app)
#toolbar.update()
#canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)   
#
#
#
#ani = animation.FuncAnimation(f2, animate, fargs = [q_min, a, a_txt, ax_h], interval=1000)
##ani2 = animation.FuncAnimation(f2, animate_his, fargs = [recentZenithHisto, ax_h], interval=1000)
##ani3 = animation.FuncAnimation(f2, ani_shower, fargs = [Analize.lastVector, recentShowerDetectors, a_sh])
###ani4 = animation.FuncAnimation(f2, flux_text, fargs = [q, a_txt], interval=1000)
#
#
#plt.draw()
#app.mainloop()
