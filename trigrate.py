import os
import numpy as np
import re
from Analysis import Analysis
import matplotlib.pyplot as plt
import scipy.optimize

def exp(x, m, a, b):
    return (-a * np.exp(np.array([-i for i in x]) * m) + b)

def function(dir, wlen):
    #closed
    depths = ['49', '54', '59', '62']

    timelistc = []
    timestampc = []
    ratelistc1 = []
    # ratelistc2 = []
    # ratelistc6 = []
    depthc = []

    #128 nm
    timelisto = []
    timestampo = []
    ratelisto1 = []
    # ratelisto2 = []
    # ratelisto6 = []
    deptho = []

    channelID = [1, 2, 4, 5, 6]

    for filename in os.listdir(dir):
        # Finds time in seconds from first timestamp
        t = re.split("_", filename)

        #Closed
        if t[1][:6] == 'closed':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timelistc.append(time)
            timestampc.append(t[:8])
            depthc.append(t[0][:2])
            # Finds Trigger Rate
            ana = Analysis(wlen)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            ratelistc1.append(trigrate[0])
            # ratelistc2.append(trigrate[1])
            # ratelistc6.append(trigrate[4])

        #128 nm
        if t[1][:6] == '1280A2':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timelisto.append(time)
            timestampo.append(t[:8])
            deptho.append(t[0][:2])
            # Finds Trigger Rate
            ana = Analysis(wlen)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            ratelisto1.append(trigrate[0])
            # ratelisto2.append(trigrate[1])
            # ratelisto6.append(trigrate[4])

    # timelistc, timestampc, ratelistc1, ratelistc2, ratelistc6, depthc = zip(*sorted(zip(timelistc, timestampc, ratelistc1, ratelistc2, ratelistc6, depthc)))
    # timelisto, timestampo, ratelisto1, ratelisto2, ratelisto6, deptho = zip(*sorted(zip(timelisto, timestampo, ratelisto1, ratelisto2, ratelisto6, deptho)))

    x = []
    y = []

    xc = []
    ytesto = []
    ytestc = []

    for j in range(len(timelisto)):
        stuff = abs(np.array(timelistc) - timelisto[j])
        index = stuff.argmin()
        x.append(timelisto[j])
        y.append(ratelisto1[j] - ratelistc1[index])
        # print(i, x, y)

        xc.append(timelistc[index])
        ytesto.append(ratelisto1[j])
        ytestc.append(ratelistc1[index])

    x, xc, ytesto, ytestc, deptho = zip(*sorted(zip(x, xc, ytesto, ytestc, deptho)))
    for i in range(len(ytesto)):
        print(x[i], ytesto[i], xc[i], ytestc[i], deptho[i])


# function("C:\\Users\\lzvio\\20231005_measurement\\", 1280)
# function("C:\\Users\\lzvio\\20231006_measurement\\", 1280)
# function("C:\\Users\\lzvio\\20231009_measurement\\", 1280)
function("C:\\Users\\lzvio\\20231010_measurement\\", 1280)


# Day 1 Fit Parameters: [1.47938280e-04 1.48632302e+02 2.66501532e+02]
# Day 2 Fit Parameters: [3.93767742e-04 1.09954282e+02 2.32693275e+02]
# Day 3 Fit Parameters: [-1.76998555e-03 -5.67332915e-02  3.48789744e+01]