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
threadLoop1 = threading.Thread(target = Analize.PrintZenith)
threadLoop1.start()



time.sleep(1)
##Analize.InitializeWindow()
##plt.ion()
##time.sleep(1)

##box = tk.Entry(app)
##button = tk.Button(app, text="check", command=self.plot)
##fr = tk.Frame()


app = tk.Tk()
def end_fullscreen(event = None):
    app.attributes("-fullscreen", False)
    return "break"

app.bind("<Escape>", end_fullscreen)
app.attributes("-fullscreen", True)
f2 = plt.figure()
gs = gridspec.GridSpec(3,3)
a = f2.add_subplot(gs[0,:-1])
a_txt = f2.add_subplot(gs[0,-1])
##a_sh = f2.add_subplot(gs[1:,:-1], projection='3d')
a_r = f2.add_subplot(gs[1:,:-1])
ax_h = f2.add_subplot(gs[-1, -1])
a_txt2 = f2.add_subplot(gs[1,-1])

plt.ion()



canvas = FigureCanvasTkAgg(f2, master = app)
canvas.show()

canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2TkAgg(canvas, app)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)   



ani = animation.FuncAnimation(f2, animate, fargs = [Analize.q, a, a_txt, ax_h, a_r, a_txt2], interval=5000)
##ani2 = animation.FuncAnimation(f2, animate_his, fargs = [recentZenithHisto, ax_h], interval=1000)
##ani3 = animation.FuncAnimation(f2, ani_shower, fargs = [Analize.lastVector, recentShowerDetectors, a_sh])
##ani4 = animation.FuncAnimation(f2, flux_text, fargs = [q, a_txt], interval=1000)


plt.draw()
app.mainloop()
