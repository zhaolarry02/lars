import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import os
import re
from Analysis import Analysis

def exp(x, m, a, b): # exponential function for curve fit
    return (a * np.exp(np.array([-i for i in x]) * m) + b)

def function(dir, wlen): # main function for scattering length analysis
    depths = [20, 17, 14, 11] # LAr depth in in

    closed = [] # contains a sublist of format [time (s), depth, rate] for each shutter closed file
    wvopen = [] # above, but for each shutter open file

    channelID = [1, 2, 4, 5, 6]
    ana = Analysis(wlen) # import Analysis function (Github)

    for filename in os.listdir(dir): # Finds time in seconds        
        t = re.split("_", filename) # Split file title

        #Closed
        if t[1][:6] == 'closed':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            # Finds Trigger Rate
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            closed.append([time, t[0][:2], trigrate[0]]) # time in seconds, depth in inch, trigger rate

        #128 nm
        if t[1][:4] == str(wlen):
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            # Finds Trigger Rate
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            wvopen.append([time, t[0][:2], trigrate[0]]) # time in seconds, depth in inch, trigger rate
    sorted(closed, key=lambda x: x[0])
    
    signal = []

    for k in depths:
        for i in range(len(wvopen)):
            closedindex = []
            for j in range(len(closed)):
                if wvopen[i][1] == closed[j][1]: #if open depth = closed depth
                    closedindex.append(j)
                    timediff = abs(wvopen[i][0] - closed[j][0])
                    index = timediff.argmin()
                    signal.append(wvopen[i][2] - [index])

function("C:\\Users\\lzvio\\20231025_lightsource_cali\\", 1280)
