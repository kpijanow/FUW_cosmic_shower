'''
FUW_cosmic_shower
    main.py
deals with multiple threads
'''

import analize
import threading
import time
import tkinter as tk
##import Image
##import numpy as np
import matplotlib.image as mpimg

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

app = tk.Tk()
def end_fullscreen(event = None):
    app.attributes("-fullscreen", False)
    return "break"

app.bind("<Escape>", end_fullscreen)
app.attributes("-fullscreen", True)

##im = Image.open('/home/pi/Desktop/FUW_cosmic_shower/quarklogo.png')
##im = np.array(im).astype(np.float) / 255
##im = plt.imread("/home/pi/Desktop/FUW_cosmic_shower/quarklogo.png")

f2 = plt.figure()
##f2.figimage(im, fig.bbox.xmax - im.size[0], fig.bbox.ymax - im.size[1])
gs = gridspec.GridSpec(3,3)
a = f2.add_subplot(gs[0,:-1])                       #flux in time
a_txt = f2.add_subplot(gs[1:,-1])                    #description
a_png = f2.add_subplot(gs[0,-1])
a_sh = f2.add_subplot(gs[1,:-1], projection='3d')   #3d projection
a_r = f2.add_subplot(gs[2,0])                    #shower radious
ax_h = f2.add_subplot(gs[2,1])                   #zenith
##a_txt2 = f2.add_subplot(gs[1,-1])                   #nobody knows
plt.ion()

canvas = FigureCanvasTkAgg(f2, master = app)
canvas.show()

canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2TkAgg(canvas, app)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)   

ani = animation.FuncAnimation(f2, animate, fargs = [Analize.q, a, a_txt, ax_h, a_r, a_sh, a_png], interval=5000)

plt.draw()
app.mainloop()
