import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import os
import re
from Analysis import Analysis

def exp(x, m, a, b): # exponential function for curve fit
    return (a * np.exp(np.array([-i for i in x]) * m) + b)

def function(dirs):
    depth = [60, 55, 50, 45, 40, 35, 30, 26, 25, 21, 17, 14, 12]
    depthcm = [128.0970994, 114.9495949, 102.4368448, 89.3539062, 76.68776733, 64.50960174, 51.8504376, 42.32291091, 39.6549546, 27.42838632, 17.6438245, 9.824104101, 4.674364388]
    channelID = [1] # [1, 2, 4, 5, 6]
    wavelength = [128] # [124, 125, 126, 127, 128, 129, 130, 131, 132] 142, 152, 173, 174, 175, 176, 177, 178, 179, 180]
    ana = Analysis(1280)
    mainlist = []

    for dir in dirs:
        for filename in os.listdir(dir):        
            t = re.split("_", filename) # Split file title

            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8]) # Time in seconds since midnight
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID) # Finds Trigger Rate
            mainlist.append([time, t[0][:2], t[1][:3], trigrate[0]]) # time in seconds, depth, wavelength, trigger rate
        
    closed = [mainlist[i] for i in range(len(mainlist)) if mainlist[i][2] == 'clo']
    bkgdlist = []

    for d in depth:
        bkgd = np.mean([closed[i][3] for i in range(len(closed)) if float(closed[i][1]) == d])
        bkgdlist.append([d, bkgd])
    for wv in wavelength:
        opened = [mainlist[i] for i in range(len(mainlist)) if mainlist[i][2] == str(wv)]
        wvlsignal = [] 
        for d in range(len(depth)):
            signal = np.mean([i[3] - bkgdlist[d][1] for i in opened if float(i[1]) == depth[d]])
            wvlsignal.append(signal)
        plt.scatter(depthcm, wvlsignal)
        plt.title(str(wv)+str(channelID))
        par, cov = scipy.optimize.curve_fit(exp, depthcm[:8], wvlsignal[:8], p0=[1/125, 115, 25], maxfev=100000)
        plt.plot(depthcm[:8], exp(depthcm[:8], *par), label='l = '+str(round(1/par[0], 2)))
        plt.legend()
        # plt.savefig("C:\\Users\\lzvio\\Scattering Length Curve Fit Plot\\Length_Fit"+str(wv))
        plt.ylim(ymin=0)
        plt.xlabel('LAr Depth (cm)')
        plt.ylabel('Ch 1 Trigger Rate')
        plt.show()
        # print(wvlsignal)

    


# function(["C:\\Users\\lzvio\\20231107\\"])
function(["C:\\Users\\lzvio\\20231110\\", "C:\\Users\\lzvio\\20231107\\", "C:\\Users\\lzvio\\20231108\\", "C:\\Users\\lzvio\\20231109\\", "C:\\Users\\lzvio\\20231111\\"])
