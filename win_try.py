import matplotlib.animation as animation
from matplotlib import gridspec
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

import numpy as np
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
import textwrap


from vec import det_plot
import time
import datetime
import matplotlib.dates as mdates
from threading import Lock

def ani_shower(i, vec_t, vec_d, a_sh):	
        try:    
                a_sh.clear()        
        ##        print("det_plot")
                rot = det_plot(vec_t,vec_d, a_sh)
                a_sh.set_xlabel("m", fontsize = 14)
                a_sh.set_ylabel("m", fontsize = 14)
                a_sh.set_zlabel("time of arival [ns]", fontsize = 12) 
                rot.view_init(elev = 30, azim = -75) #i%360)
        except Exception as e:
                with open("error.txt", "a") as errFile:
                        errFile.write(e)
                        print(e.args)
                return

def animate(i, q_min, a, a_txt, ax_h, a_r, a_sh, a_png):#, a_txt2):
        try:
##                print("IN ANIMATE")
                xar=[]

##                mutex = Lock()
##                mutex.acquire()
                while(q_min.full() != True):
                        return
                
                tableOfFluxInEveryMinute = q_min.get_nowait()
                txt = round(q_min.get_nowait(),4)
                recentZenithHisto = q_min.get_nowait()
                recentRadiusHisto = q_min.get_nowait()
                recentDetectors = q_min.get_nowait()
                recentVector = q_min.get_nowait()
                recentArrivalTimes = q_min.get_nowait()
##                mutex.release()

                timeBin = 120
                
                if len(tableOfFluxInEveryMinute) != timeBin:
        ##                print("not 60: " + str(tableOfFluxInEveryMinute))
                        time.sleep(2)
                        return

                localtime = time.localtime(time.time())
                minuteS = 24 * 60 / timeBin
                xar = [datetime.datetime.now() - datetime.timedelta(hours=24) + datetime.timedelta(minutes=minuteS) * i for i in range(timeBin)]

                a.clear()
                myFmt = mdates.DateFormatter('%H:%M')        
                a.xaxis.set_major_formatter(myFmt)
                a.set_xlabel("time", fontsize = 16)
                a.set_ylabel("flux [$cm^{-2} min^{-1}$]", fontsize = 16)
                a.set_title("Cosmic muon flux in time", fontsize = 20)
                
                #print(tableOfFluxInEveryMinute)
                a.plot(xar, tableOfFluxInEveryMinute)
                #a.autofmt_xdate()
                
                a_txt.clear()
                a_txt.axis('off') 
                a_txt.text(0.5,1.15, "Cosmic Muon Monitor", horizontalalignment='center',
                verticalalignment='top', fontsize = 35,
                transform=a_txt.transAxes)
                text = ' '.join(['Four scintillators provided by QuarkNet placed above us monitor cosmic muons and air showers. Positions of the detecors is visualized on the',
                        '3D plot on the left. The vertical line indicates the time of arival of the muon to the detector in nanoseconds. This time difference allows us',
                        'to calculate the zenith angle at which the shower came. The distance between the detectors that fired give us an information about the',
                        'minimal radius of the shower. We are expecting one shower about every few minutes.'])
                        
                a_txt.text(0.5,0.8, textwrap.fill(text, 45),
                           horizontalalignment='center', verticalalignment='top', fontsize = 17, transform=a_txt.transAxes)
                a_txt.text(0.5,1.0, "Mean value of flux from\n total acquisition time:",
                           horizontalalignment='center', verticalalignment='top', fontsize = 22, transform=a_txt.transAxes)
                a_txt.text(0.5,0.89, str(txt)+" [$cm^{-2} min^{-1}$]",
                           horizontalalignment='center', verticalalignment='top', fontsize = 22, weight = "bold", transform=a_txt.transAxes)
                a_txt.text(1,0.1, "Made by: \n Karol Pijanowski, Karolina Rozwadowska, Katarzyna Wojczuk \n as a part of the classes Zaspołowy projekt studencki",
                           horizontalalignment='right', verticalalignment='top', fontsize = 10, transform=a_txt.transAxes)

                img1 = mpimg.imread('/home/pi/Desktop/FUW_cosmic_shower/quarklogo.png')
                a_png.clear()
                a_png.axis('off') 
                a_png.imshow(img1)

##                a_txt2.clear()
##                a_txt2.axis('off') 
                
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
                ax_h.set_xticks(indZ, minor = False)
                ax_h.set_xticklabels(labelsZ)
                ax_h.bar(indZ, zen, color = 'orange', width = 1)
                ax_h.set_title("Zenith angle distribution", fontsize = 20)
                ax_h.set_xlabel("degrees", fontsize = 16)
                ax_h.set_ylabel("normalized counts", fontsize = 16)
                
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
                a_r.set_title("Minimum radius distribution", fontsize = 20)
                a_r.bar(indR, rad, color='red', width = 1)
                a_r.set_xlabel("radius [m]", fontsize = 16)
                a_r.set_ylabel("normalized counts", fontsize = 16)
                ani_shower(i, recentArrivalTimes, recentDetectors, a_sh)
##                print("OUT OF ANIMATE")
        except Exception as e:
                with open("error.txt", "a") as errFile:
                        errFile.write(e)
                        print(e.args)
                return

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
        
