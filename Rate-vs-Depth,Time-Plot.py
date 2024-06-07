# 3 functions produce: 1. plot of SiPM Trigger Rate versus vertical distance from Liquid Argon surface to SiPM, 2. plot SiPM Trigger Rate versus Liquid Argon Depth and curve fit, 3. plot nackground subtracted trigger rate versus time.

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import os
import re
from Analysis import Analysis # Use functions defined in 'Analysis' python script written by Dr. Mu Wei, Dr. Alex Himmel, and Larry Zhao

def exp(x, m, a, b): # exponential function for curve fit
    return (a * np.exp(np.array([-i for i in x]) * m) + b)


# Plot SiPM Trigger Rate versus vertical distance from Liquid Argon surface to SiPM
def ratevsSiPMdepth(dirs):
    depth = [60, 55, 50, 45, 40, 35, 30, 26, 25, 21, 17, 14, 12] # depth in inches
    depthcm = [128.0970994, 114.9495949, 102.4368448, 89.3539062, 76.68776733, 64.50960174, 51.8504376, 42.32291091, 39.6549546, 27.42838632, 17.6438245, 9.824104101, 4.674364388] # depth in centimeters
    channelID = [1, 2, 4, 5]
    # wavelength = [124, 125, 126, 127, 128, 129, 130, 131, 132, 142, 152, 173, 174, 175, 176, 177, 178, 179, 180] # wavelength in nanometers
    wvl = 128 # Argon scintillation peak wavelength in nanometers
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

    opened = [mainlist[i] for i in range(len(mainlist)) if mainlist[i][2] == str(wvl)]

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


# Plot SiPM Trigger Rate versus Liquid Argon Depth and curve fit
def ratevsLArdepthfit(dirs):
    depth = [60, 55, 50, 45, 40, 35, 30, 26, 25, 21, 17, 14, 12] # depth in inches
    depthcm = [128.0970994, 114.9495949, 102.4368448, 89.3539062, 76.68776733, 64.50960174, 51.8504376, 42.32291091, 39.6549546, 27.42838632, 17.6438245, 9.824104101, 4.674364388] # depth in centimeters
    channelID = [1] # [1, 2, 4, 5]
    wavelength = [128] # [124, 125, 126, 127, 128, 129, 130, 131, 132, 142, 152, 173, 174, 175, 176, 177, 178, 179, 180] # wavelength in nanometers
    ana = Analysis(1280)

    mainlist = []

    for dir in dirs:
        for filename in os.listdir(dir):        
            t = re.split("_", filename) # Split file title
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8]) # Calculate time in seconds since time 00:00:00 of data collection date
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID) # Calculate Trigger Rate in Hertz via 'Analysis' script trigger rate function
            mainlist.append([time, t[0][:2], t[1][:3], trigrate[0]]) # sublist contains time (s), depth (in), wavelength (nm), trigger rate (Hz) for Channel 1
        
    closed = [mainlist[i] for i in range(len(mainlist)) if mainlist[i][2] == 'clo'] # Shutter closed data (background signals only)
    bkgdlist = []

    for d in depth:
        bkgd = np.mean([closed[i][3] for i in range(len(closed)) if float(closed[i][1]) == d]) # background trigger rate at depth d
        bkgdlist.append([d, bkgd])

    for wvl in wavelength:
        opened = [mainlist[i] for i in range(len(mainlist)) if mainlist[i][2] == str(wvl)]
        wvlsignal = [] 
        for d in range(len(depth)):
            signal = np.mean([i[3] - bkgdlist[d][1] for i in opened if float(i[1]) == depth[d]])
            wvlsignal.append(signal)
        

        plt.title(str(wvl)+str(channelID))
        plt.scatter(depthcm, wvlsignal)
        par, cov = scipy.optimize.curve_fit(exp, depthcm[:8], wvlsignal[:8], p0=[1/125, 115, 25], maxfev=100000)
        plt.plot(depthcm[:8], exp(depthcm[:8], *par), label='l = '+str(round(1/par[0], 2)))
        plt.xlabel('LAr Depth (cm)')
        plt.ylabel('Ch 1 Trigger Rate')
        plt.ylim(ymin=0)
        plt.grid()
        plt.legend()
        plt.show()
        # plt.savefig("<save directory>"+"Length_Fit"+str(wvl)+".png")
        # print(wvlsignal)


# Plot Shutter Open Time versus Shutter Open Rates subtracted by closest timestamp Background Rate
def bkgdsubvtime(dir, wvl): # main function for scattering length analysis
    depths = [20, 17, 14, 11] # LAr depth in in
    channelID = [1, 2, 4, 5, 6]
    ana = Analysis(wvl) # import Analysis function (Github)

    closed = [] # contains sublist [time (s), depth (in), rate (Hz)] for each shutter closed file
    opened = [] # contains sublist [time (s), depth (in), rate (Hz)] for each shutter open file
    opened_time = [] #  List of time in seconds since time 00:00:00 of data collection date for each data file

    for filename in os.listdir(dir): # Finds time in seconds        
        t = re.split("_", filename) # Split file title

        #Closed
        if t[1][:6] == 'closed':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            closed.append([time, t[0][:2], trigrate[0]]) # time (s), depth (in), trigger rate (Hz) for Channel 1

        #Opened
        if t[1][:4] == str(wvl):
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            opened_time.append(time)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            opened.append([time, t[0][:2], trigrate[0]]) # time (s), depth (in), trigger rate (Hz) for Channel 1
    
    sorted(closed, key=lambda x: x[0]) # Sort shutter closed files by timestamp
    sorted(opened, key=lambda x: x[0]) # Sort shutter opened files by timestamp
    

    signal = []

    for i in range(len(opened)):
        timedifflist = []
        for j in range(len(closed)):
            if opened[i][1] == closed[j][1]: #if opened depth = closed depth
                timediff = abs(opened[i][0] - closed[j][0]) # absolute difference between opened timestamp and closed timestamp 
                timedifflist.append(timediff)
        index = np.argmin(timedifflist)
        signal.append(opened[i][2] - closed[index][2])


    plt.title(str(wvl)+' Rate minus Background v Time')
    plt.scatter(opened_time, signal)
    plt.xlabel('Time (s) since 00:00:00 of data collection date')
    plt.ylabel('Ch 1 Background Subtracted Trigger Rate')
    plt.grid()
    plt.show()


ratevsSiPMdepth([<list of data file directories>])
ratevsLArdepthfit([<list of data file directories>])
bkgdsubvtime("C:\\...\\20231025_lightsource_cali\\", 1280)
