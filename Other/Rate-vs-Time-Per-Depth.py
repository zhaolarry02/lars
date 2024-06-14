import os
import numpy as np
import re
from Analysis import Analysis
import matplotlib.pyplot as plt
import scipy.optimize

def exp(x, m, a, b):
    return (-a * np.exp(np.array([-i for i in x]) * m) + b)

def function(dir, wvl):
    ana = Analysis(wvl)
    
    #closed
    depths = ['49', '54', '59', '62']

    timeclosed = []
    rateclosed1 = []
    rateclosed2 = []
    rateclosed6 = []
    depthclosed = []

    #Opened
    timeopened = []
    rateopened1 = []
    rateopened2 = []
    rateopened6 = []
    depthopened = []

    channelID = [1, 2, 4, 5, 6]

    for filename in os.listdir(dir):
        t = re.split("_", filename)

        #Closed
        if t[1][:6] == 'closed':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timeclosed.append(time)
            depthclosed.append(t[0][:2])
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            rateclosed1.append(trigrate[0])
            rateclosed2.append(trigrate[1])
            rateclosed6.append(trigrate[4])

        #Opened
        if t[1][:4] == str(wvl):
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timeopened.append(time)
            depthopened.append(t[0][:2])
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            rateopened1.append(trigrate[0])
            rateopened2.append(trigrate[1])
            rateopened6.append(trigrate[4])

    timeclosed, rateclosed1, rateclosed2, rateclosed6, depthclosed = zip(*sorted(zip(timeclosed, rateclosed1, rateclosed2, rateclosed6, depthclosed)))
    timeopened, rateopened1, rateopened2, rateopened6, depthopened = zip(*sorted(zip(timeopened, rateopened1, rateopened2, rateopened6, depthopened)))

    #Plot Ch 1 Shutter Open Rate per Level
    for i in depths:
        x = []
        y = []
        for j in range(len(depthopened)):
            if depthopened[j] == i:
                x.append(timeopened[j])
                y.append(rateopened1[j])
                print(i, depthopened[j])
        plt.scatter(np.array(x)-min(x), y)
        plt.title('Depth = '+str(i))
        plt.savefig('C:\\...\\Depth'+str(i)+'.png')

    #Plot Ch 1 Shutter Open Rate minus Nearest Background, per Level
    for i in depths:
        x = []
        y = []
        for j in range(len(depthopened)):
            if depthopened[j] == i:
                timediff = abs(np.array(timeclosed) - timeopened[j])
                index = timediff.argmin()
                # print(timeclosed[index], timeopened[j])
                x.append(timeopened[j])
                y.append(rateopened1[j] - rateclosed1[index])
        # print(i, x, y)
        plt.scatter(x, y)
        plt.ylim(0, 100)
        plt.title('Depth = '+str(i))
        plt.show()
        plt.savefig('C:\\...\\Depth'+str(i)+'-Background.png')
        x.clear()
        y.clear()

    # Plot all Ch 1 Shutter Opened Rate minus Nearest Background, from one day
    x = []
    y = []

    xc = []
    ytesto = []
    ytestc = []

    for j in range(len(timeopened)):
        timediff = abs(np.array(timeclosed) - timeopened[j])
        index = timediff.argmin()
        x.append(timeopened[j])
        y.append(rateopened1[j] - rateclosed1[index])

        xc.append(timeclosed[index])
        ytesto.append(rateopened1[j])
        ytestc.append(rateclosed1[index])

    x, xc, ytesto, ytestc = zip(*sorted(zip(x, xc, ytesto, ytestc)))
    for i in range(len(ytesto)):
        print(x[i], ytesto[i], xc[i], ytestc[i])

    x = np.array(x)-min(x)

    plt.scatter(x, y)
    plt.ylim(0, 120)
    par, cov = scipy.optimize.curve_fit(exp, x, y, p0=[6.53*10**(-5), 1.04*10**(2), 1.24*10**(2)], maxfev=100000)
    plt.plot(x, exp(x, *par))
    plt.title('Month, Day='+str(dir[19:23])+', Par: '+str(par[0])+', '+str(round(par[1], 2))+', '+str(np.round(par[2], 2)))
    plt.show()
    print(par)

#     # To plot begin/end from multiple days
#     x = []
#     y = []
#     for j in range(len(timeopened)):
#         timediff = abs(np.array(timeclosed) - timeopened[j])
#         index = timediff.argmin()
#         x.append(timeopened[j])
#         y.append(rateopened1[j] - rateclosed1[index])
#         # print(i, x, y)
#     x, y = zip(*sorted(zip(x, y)))
#     times.append(x[0])
#     times.append(list(x).pop())
#     rates.append(y[0])
#     rates.append(list(y).pop())
# times = []
# rates = []
# # Call function here with each day's folder path
# times = np.array(times)
# times[2:4] = times[2:4]+24*3600
# times[4:6] = times[2:4]+24*3600*2
# times[6:8] = times[2:4]+24*3600*3
# plt.scatter(times, rates)
# plt.title('First and Last '+str(wvl)+' nm Intensity Per Day')
# plt.show()

# function("C:\\...\\20231005_measurement\\", 1280)
# function("C:\\...\\20231006_measurement\\", 1280)
# function("C:\\...\\20231009_measurement\\", 1280)
# function("C:\\...\\20231010_measurement\\", 1280)
