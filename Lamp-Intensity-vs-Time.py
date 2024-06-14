# Plot of lamp intensity versus time. Channel 1, 2 for submerged bottom and side SiPM, and Channel 6 for unsubmerged SiPM.

import os
import numpy as np
import re
from Analysis import Analysis
import matplotlib.pyplot as plt
import scipy.optimize

def log(x, a, b, c):
    return (a * np.log(x * b) + c)

def exp(x, m, a, b):
    return (-a * np.exp(np.array([-i for i in x]) * m) + b)

def lin(x, m, b):
    return (m*x + b)

def lampintensityplot(dir, wvl):
    ana = Analysis(wvl)

    #Closed
    timeclosed = []
    rateclosed1 = []
    rateclosed2 = []
    rateclosed6 = []

    #Opened
    timeopened = []
    rateopened1 = []
    rateopened2 = []
    rateopened6 = []


    channelID = [1, 2, 4, 5, 6]

    for filename in os.listdir(dir):
        # Finds time in seconds from first timestamp
        t = re.split("_", filename)

        #Closed
        if t[1][:6] == 'closed':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timeclosed.append(time)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)

            rateclosed1.append(trigrate[0])
            rateclosed2.append(trigrate[1])
            rateclosed6.append(trigrate[4])
                # date_object = datetime.strptime(t[2][2:10]+' '+t[3][:8], "%y-%m-%d %H-%M-%S")
                # timeclosed.append(date_object)

        #Opened
        if t[1][:4] == str(wvl):
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timeopened.append(time)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)

            rateopened1.append(trigrate[0])
            rateopened2.append(trigrate[1])
            rateopened6.append(trigrate[4])

    timeclosed, rateclosed1, rateclosed2, rateclosed6 = zip(*sorted(zip(timeclosed, rateclosed1, rateclosed2, rateclosed6)))
    timeopened, rateopened1, rateopened2, rateopened6 = zip(*sorted(zip(timeopened, rateopened1, rateopened2, rateopened6)))

    num = len(timeclosed)
    backgroundc1 = [(sum(rateclosed1[i:i+2])/2) for i in range(0, num, 2)]
    backgroundc2 = [(sum(rateclosed2[i:i+2])/2) for i in range(0, num, 2)]
    backgroundc6 = [(sum(rateclosed6[i:i+2])/2) for i in range(0, num, 2)]

    rateopened1 = list(rateopened1)
    rateopened2 = list(rateopened2)
    rateopened6 = list(rateopened6)


    for i in range(len(timeopened)):
        rateopened1[i] = rateopened1[i] - backgroundc1[i//3]
        rateopened2[i] = rateopened2[i] - backgroundc2[i//3]
        rateopened6[i] = rateopened6[i] - backgroundc6[i//3]


    # Closed
    timestampclosed = np.array(timeclosed) - min(timeclosed)
    plt.scatter(timestampclosed, rateclosed1, c='b', label='Ch 1')
    plt.scatter(timestampclosed, rateclosed2, c='g', label='Ch 2')
    plt.scatter(timestampclosed, rateclosed6, c='r', label='Ch 6')
    plt.title('Closed')
    plt.xlabel('Time (s)')
    plt.ylabel('Trigger Rate (Hz)')
    plt.ylim(0, 175)
    plt.grid()
    plt.legend(loc='upper left')
    plt.show()
    
    #Opened
    timestampopened = np.array(timeopened) - min(timeopened)
    plt.scatter(timestampopened, rateopened1, c='b', label='Ch 1')
    plt.scatter(timestampopened, rateopened2, c='g', label='Ch 2')
    plt.scatter(timestampopened, rateopened6, c='r', label='Ch 6')
    plt.title(str(wvl)+' nm')
    plt.xlabel('Time (s)')
    plt.ylabel('Trigger Rate (Hz)')
    plt.ylim(0, 400)
    plt.grid()
    plt.legend(loc='upper left')

    par, cov = scipy.optimize.curve_fit(lin, timestampopened, rateopened1, p0=[1.22*10**(-3), 3.45*10], maxfev=100000)
    plt.plot(timestampopened, lin(timestampopened, *par))
    plt.title('Test Rate vs Time'+str(par))
    plt.ylim(0, 50)
    plt.show()

    print(par)
    print(scipy.stats.pearsonr(timestampopened, lin(timestampopened, *par)))

lampintensityplot("C:/.../Day3_RatevTime/", 1280)

# Day 1 Fit Parameters: [1.47938280e-04 1.48632302e+02 2.66501532e+02]
# Day 2 Fit Parameters: [3.93767742e-04 1.09954282e+02 2.32693275e+02]
# Day 3 Fit Parameters: [-1.76998555e-03 -5.67332915e-02  3.48789744e+01]
