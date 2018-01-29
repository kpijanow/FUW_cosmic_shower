import matplotlib.animation as animation
from matplotlib import gridspec
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

import numpy as np
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from vec import det_plot
import time
import datetime
import matplotlib.dates as mdates



def animate(i, q_min, a, a_txt, ax_h, a_r):
##        print("IN ANIMATE")
        xar=[]

        while(q_min.full() != True):
                return
                time.sleep(0.0001)
##        if q_min.unfinished_tasks():
##                print("UNFINISHED")
##                return
        
        tableOfFluxInEveryMinute=q_min.get_nowait()
        txt=round(q_min.get_nowait(),4)
        recentZenithHisto=q_min.get_nowait()
        recentRadiousHisto = q_min.get_nowait()

        timeBin = 120
                
        if len(tableOfFluxInEveryMinute) != timeBin:
##                print("not 60: " + str(tableOfFluxInEveryMinute))
                time.sleep(2)
                return

        localtime = time.localtime(time.time())
        minuteS = 24 * 60 / timeBin
        xar = [datetime.datetime.now() + datetime.timedelta(minutes=minuteS) * i for i in range(timeBin)]

        myFmt = mdates.DateFormatter('%H:%M')
        a.xaxis.set_major_formatter(myFmt)
        a.clear()
        #print(tableOfFluxInEveryMinute)
        a.plot(xar, tableOfFluxInEveryMinute)
        #a.autofmt_xdate()
        a_txt.clear()
        a_txt.axis('off')
        a_txt.text(0.7,1, "QNet", horizontalalignment='right',
        verticalalignment='top', fontsize = 60,
        transform=a_txt.transAxes)
        a_txt.text(0.7,0.5, txt, horizontalalignment='right',
        verticalalignment='top', fontsize = 40,
        transform=a_txt.transAxes)
        ax_h.clear()
        #ind = np.arange(len(recentZenithHisto))
        ind = ["0", "10", "20", "30", "40", "60", "80"]
        ax_h.bar(ind, recentZenithHisto, color='orange')
        a_r.clear()
        indR = [2, 3, 4, 5, 6, 9]
        a_r.bar(indR, recentRadiousHisto, color='red')
##        print("OUT OF ANIMATE")

def ani_shower(i, vec_t, vec_d, a_sh):	
	
        a_sh.clear()	
        print(vec_t)
        rot = det_plot(vec_t,vec_d, a_sh)
        rot.view_init(elev = 30, azim = i%360)

def animate_his(i, recentZenithHisto, ax_h):

	ax_h.clear()
	ind = np.arange(len(recentZenithHisto))
	ax_h.bar(ind, recentZenithHisto, color='orange')


def flux_text(i, in_q, a_txt):
	
        txt=round(in_q.get(),4)
        a_txt.clear()
        a_txt.axis('off')
        a_txt.text(0.7,1, "QNet", horizontalalignment='right',
        verticalalignment='top', fontsize = 60,
        transform=a_txt.transAxes)
        a_txt.text(0.7,0.5, txt, horizontalalignment='right',
        verticalalignment='top', fontsize = 40,
        transform=a_txt.transAxes)
        
