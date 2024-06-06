# Plot SiPM Trigger Rate versus vertical distance from Liquid Argon surface to SiPM

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import os
import re
from Analysis import Analysis # Use functions defined in 'Analysis' python script written by Dr. Mu Wei, Dr. Alex Himmel, and Larry Zhao

def exp(x, m, a, b): # exponential function for curve fit
    return (a * np.exp(np.array([-i for i in x]) * m) + b)

def function(dirs):
    depth = [list of liquid argon depth meter readings] # in inches
    depthcm = [list of liquid argon depth meter readings] # in centimeters
    channelID = [1, 2, 4, 5]
    # wavelength = [124, 125, 126, 127, 128, 129, 130, 131, 132, 142, 152, 173, 174, 175, 176, 177, 178, 179, 180] # wavelength in nanometers
    wv = 128 # Argon scintillation peak wavelength in nanometers
    ana = Analysis(1280)
    
    mainlist = []
    for dir in dirs:
        for filename in os.listdir(dir):        
            t = re.split("_", filename) # Split file title
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8]) # Calculate time in seconds since time 00:00:00 of data collection date
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID) # Calculate Trigger Rate in Hertz via 'Analysis' script trigger rate function
            mainlist.append([time, t[0][:2], t[1][:3], trigrate[0], trigrate[1], trigrate[2], trigrate[3]]) # sublist contains time (s), depth (in), wavelength (nm), trigger rates (Hz) for Channel 1, 2, 4, 5
        
    closed = [mainlist[i] for i in range(len(mainlist)) if mainlist[i][2] == 'clo'] # Shutter closed data (background signals only)
    bkgdlist = []

    for d in depth:
        bkgd1 = [] # Ch 1
        bkgd2 = [] # Ch 2
        bkgd4 = [] # Ch 4
        bkgd5 = [] # Ch 5
        for i in range(len(closed)):
            if float(closed[i][1]) == d:
                bkgd1.append([closed[i][3]])
                bkgd2.append([closed[i][4]])
                bkgd4.append([closed[i][5]])
                bkgd5.append([closed[i][6]])
        bkgdlist.append([np.mean(bkgd1), np.mean(bkgd2), np.mean(bkgd4), np.mean(bkgd5)])

    opened = [mainlist[i] for i in range(len(mainlist)) if mainlist[i][2] == str(wv)]

    sipmz = [25.75968709, 46.25968709, 65.25968709, 143.5596871] # SiPM Depth in centimeters
    color = ['c', 'r', 'b', 'g']
    # colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive']

    for d in range(len(depth)):
        signal1 = [] # Ch 1
        signal2 = [] # Ch 2
        signal4 = [] # Ch 3
        signal5 = [] # Ch 4
        wvlsignal = []
        
        for i in opened:
            if float(i[1]) == depth[d]:
                signal1.append([i[3] - bkgdlist[d][0]])
                signal2.append([i[4] - bkgdlist[d][1]])
                signal4.append([i[5] - bkgdlist[d][2]])
                signal5.append([i[6] - bkgdlist[d][3]])
        
        sipmz2 = [depthcm[d], depthcm[d]-46.25968709+25.75968709, depthcm[d]-65.25968709+25.75968709, depthcm[d]-143.5596871+25.75968709]
        wvlsignal.append([np.mean(signal1), np.mean(signal2), np.mean(signal4), np.mean(signal5)])
        plt.scatter(sipmz2, wvlsignal, c=color) # , label=str(depth[d])
        # plt.title(str(depthcm[d])+" LAr Depth (cm)")
        # plt.ylim(ymin=0)

    plt.title('Signal Rate vs SiPM Depth')
    plt.xlabel('SiPM Height (cm)')
    plt.ylabel('128 nm Trigger Rate')
    plt.ylim(0, 25)
    plt.grid()
    # plt.legend()
    plt.show()
    # plt.savefig("<save directory>"+str(depth[d])+"in. Signal vs SiPM Depth.png")

    # # Plot Ch 2 / Ch 1 rate
    # ratios = []
    # ratios.append(np.mean(signal2) / np.mean(signal1))
    # plt.scatter(depthcm, ratios)
    # plt.title('128 nm, Ch 2/Ch 1 Rate vs Depth')
    # plt.show()

function([<list of data file directories>])
