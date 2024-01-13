import os
import numpy as np
import re
# from datetime import datetime
from Analysis import Analysis
import matplotlib.pyplot as plt
import scipy.optimize

def log(x, a, b, c):
    return (a * np.log(x * b) + c)

def exp(x, m, a, b):
    return (-a * np.exp(np.array([-i for i in x]) * m) + b)

def lin(x, m, b):
    return (m*x + b)

def function(dir, wlen):
    #closed
    timelistc = []
    ratelistc1 = []
    ratelistc2 = []
    ratelistc6 = []

    #128 nm
    timelisto = []
    ratelisto1 = []
    ratelisto2 = []
    ratelisto6 = []

    #170 nm
    timelisto1 = []
    ratelisto11 = []
    ratelisto21 = []
    ratelisto61 = []

    channelID = [1, 2, 4, 5, 6]

    for filename in os.listdir(dir):
        # Finds time in seconds from first timestamp
        t = re.split("_", filename)

        #Closed
        if t[1][:6] == 'closed':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timelistc.append(time)
            # Finds Trigger Rate
            ana = Analysis(wlen)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            ratelistc1.append(trigrate[0])
            ratelistc2.append(trigrate[1])
            ratelistc6.append(trigrate[4])
                # date_object = datetime.strptime(t[2][2:10]+' '+t[3][:8], "%y-%m-%d %H-%M-%S")
                # timelistc.append(date_object)

        #128 nm
        if t[1][:6] == '1280A2':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timelisto.append(time)
            # Finds Trigger Rate
            ana = Analysis(wlen)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            ratelisto1.append(trigrate[0])
            ratelisto2.append(trigrate[1])
            ratelisto6.append(trigrate[4])

        #170 nm
        # if t[1][:6] == '1700A3':
        #     time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
        #     timelisto1.append(time)
        #     # Finds Trigger Rate
        #     ana = Analysis(wlen)
        #     df = ana.import_file(dir+filename, [])
        #     trigrate = ana.trig_rate(df, channelID)
        #     ratelisto11.append(trigrate[0])
        #     ratelisto21.append(trigrate[1])
        #     ratelisto61.append(trigrate[4])

    timelistc, ratelistc1, ratelistc2, ratelistc6 = zip(*sorted(zip(timelistc, ratelistc1, ratelistc2, ratelistc6)))
    timelisto, ratelisto1, ratelisto2, ratelisto6 = zip(*sorted(zip(timelisto, ratelisto1, ratelisto2, ratelisto6)))

    # backgroundc1 = [(sum(ratelistc1[i:i+2])/2) for i in range(0, len(ratelistc1), 2)]
    # backgroundc2 = [(sum(ratelistc2[i:i+2])/2) for i in range(0, len(ratelistc2), 2)]
    # backgroundc6 = [(sum(ratelistc6[i:i+2])/2) for i in range(0, len(ratelistc6), 2)]
    # ratelisto1 = list(ratelisto1)
    # ratelisto2 = list(ratelisto2)
    # ratelisto6 = list(ratelisto6)
    # for i in range(len(ratelisto1)):
    #     ratelisto1[i] = ratelisto1[i] - backgroundc1[i//3]
    # for i in range(len(ratelisto2)):
    #     ratelisto2[i] = ratelisto2[i] - backgroundc2[i//3]
    # for i in range(len(ratelisto6)):
    #     ratelisto6[i] = ratelisto6[i] - backgroundc6[i//3]


    # Closed
    # time_newc = np.array(timelistc) - min(timelistc)
    # plt.scatter(time_newc, ratelistc1, c='b', label='Ch 1')
    # plt.scatter(time_newc, ratelistc2, c='g', label='Ch 2')
    # plt.scatter(time_newc, ratelistc6, c='r', label='Ch 6')
    # plt.legend(loc='upper left')
    # plt.title('Closed')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Trigger Rate (Hz)')
    # plt.ylim(0, 175)
    # plt.grid()
    # plt.show()
    
    #128 nm
    time_newo = np.array(timelisto) - min(timelisto)
    plt.scatter(time_newo, ratelisto1, c='b', label='Ch 1')
    # plt.scatter(time_newo, ratelisto2, c='g', label='Ch 2')
    # plt.scatter(time_newo, ratelisto6, c='r', label='Ch 6')
    # plt.legend(loc='upper left')
    # plt.title('128 nm')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Trigger Rate (Hz)')
    # plt.ylim(0, 400)
    # plt.grid()

    par, cov = scipy.optimize.curve_fit(lin, time_newo, ratelisto1, p0=[1.22*10**(-3), 3.45*10], maxfev=100000)
    plt.plot(time_newo, lin(time_newo, *par))
    plt.title('Test Rate vs Time Day 3, Pinhole 2'+str(par))
    plt.ylim(0, 50)
    plt.show()
    print(par)
    print(scipy.stats.pearsonr(time_newo, lin(time_newo, *par)))

    #170 nm
    # time_newo1 = np.array(timelisto1) - min(timelisto1)
    # plt.scatter(time_newo1, ratelisto11, c='b', label='Ch 1')
    # plt.title('170 nm Ch 1')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Trigger Rate (Hz)')
    # plt.ylim(0, 1750)
    # plt.grid()
    # plt.show()
    # #plot Ch 1 separately from other channels
    # plt.scatter(time_newo1, ratelisto21, c='g', label='Ch 2')
    # plt.scatter(time_newo1, ratelisto61, c='r', label='Ch 6')
    # plt.legend(loc='upper left')
    # plt.title('170 nm')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Trigger Rate (Hz)')
    # plt.ylim(0, 250)
    # plt.grid()
    # plt.show()

function("C:/Users/lzvio/Day3_RatevTime/", 1280)

# Day 1 Fit Parameters: [1.47938280e-04 1.48632302e+02 2.66501532e+02]
# Day 2 Fit Parameters: [3.93767742e-04 1.09954282e+02 2.32693275e+02]
# Day 3 Fit Parameters: [-1.76998555e-03 -5.67332915e-02  3.48789744e+01]