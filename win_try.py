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



def animate(i, q_min, a, a_txt, ax_h, a_r, a_txt2):
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
        recentRadiusHisto = q_min.get_nowait()

        timeBin = 120
                
        if len(tableOfFluxInEveryMinute) != timeBin:
##                print("not 60: " + str(tableOfFluxInEveryMinute))
                time.sleep(2)
                return

        localtime = time.localtime(time.time())
        minuteS = 24 * 60 / timeBin
        xar = [datetime.datetime.now() - datetime.timedelta(hours=24) + datetime.timedelta(minutes=minuteS) * i for i in range(timeBin)]

##        a.set_xlabel("time")
##        a.set_ylabel("flux [$cm^{-2} min^{-1}$]")
##        a.set_title("Cosmic muon flux in time")
        myFmt = mdates.DateFormatter('%H:%M')        
        a.xaxis.set_major_formatter(myFmt)
        a.set_xlabel("time")
        a.set_ylabel("flux [$cm^{-2} min^{-1}$]")
        a.set_title("Cosmic muon flux in time")
        

        a.clear()
        #print(tableOfFluxInEveryMinute)
        a.plot(xar, tableOfFluxInEveryMinute)
        #a.autofmt_xdate()
        
        a_txt.clear()
        a_txt.axis('off') 
        a_txt.text(.5,1, "Cosmic Muon Monitor", horizontalalignment='center',
        verticalalignment='top', fontsize = 35,
        transform=a_txt.transAxes)
        a_txt.text(0.5,0.7, "Four scintillators provided by QuarkNet \n placed above us monitor \n cosmic muons and air showers. ", horizontalalignment='center',
        verticalalignment='top', fontsize = 18,
        transform=a_txt.transAxes)
        a_txt.text(1,0.3, "Mean value of flux from\n total acquisition time:\n"+str(txt)+" [$cm^{-2} min^{-1}$]", horizontalalignment='right',
        verticalalignment='top', fontsize = 20,
        transform=a_txt.transAxes)
        a_txt.text(1,-0.2, "Made by: \n Karol Pijanowski, Karolina Rozwadowska, Katarzyna Wojczuk \n as a part of the classes Zaspołowy projekt studencki", horizontalalignment='right',
        verticalalignment='top', fontsize = 8,
        transform=a_txt.transAxes)

        a_txt2.clear()
        a_txt2.axis('off') 
        
        #a_txt.text(0.7,0.5, txt, horizontalalignment='right',
        #verticalalignment='top', fontsize = 40,
        #transform=a_txt.transAxes)
        
        ax_h.clear()
        zen = []
        if (np.sum(recentZenithHisto)==0):
                zen = recentZenithHisto
        else:
               zen = recentZenithHisto/np.sum(recentZenithHisto)
               
        indZ = np.arange(len(recentZenithHisto))
        labelsZ = ["0", "10", "20", "30", "40", "60", "80"]
        ax_h.set_xticks(indZ, minor=False)
        ax_h.set_xticklabels(labelsZ)
        ax_h.bar(indZ, zen, color='orange', width =1)
        ax_h.set_title("Zenith angle of cosmic showers distribution")
        ax_h.set_xlabel("degrees")
        ax_h.set_ylabel("normalized counts")
        
        a_r.clear()
        rad = []
        if (np.sum(recentRadiusHisto)==0):
                rad = recentRadiusHisto
        else:
               rad = recentRadiusHisto/np.sum(recentRadiusHisto)
        indR = np.arange(len(recentRadiusHisto))
        labelsR = [2, 3, 4, 5, 6, 9]
        
        a_r.set_xticks(indR, minor=False)
        a_r.set_xticklabels(labelsR)
        a_r.set_title("Minimum radius of cosmic showers distribution")
        a_r.bar(indR, rad, color='red', width = 1)
        a_r.set_xlabel("radius [m]")
        a_r.set_ylabel("normalized counts")
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
        
