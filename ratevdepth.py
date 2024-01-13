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
    ratelistc1 = []
    # ratelistc2 = []
    # ratelistc6 = []
    depthc = []

    #128 nm
    timelisto = []
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
            deptho.append(t[0][:2])
            # Finds Trigger Rate
            ana = Analysis(wlen)
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID)
            ratelisto1.append(trigrate[0])
            # ratelisto2.append(trigrate[1])
            # ratelisto6.append(trigrate[4])

    # timelistc, ratelistc1, ratelistc2, ratelistc6, depthc = zip(*sorted(zip(timelistc, ratelistc1, ratelistc2, ratelistc6, depthc)))
    # timelisto, ratelisto1, ratelisto2, ratelisto6, deptho = zip(*sorted(zip(timelisto, ratelisto1, ratelisto2, ratelisto6, deptho)))

    #Plot per level
    # print(deptho)
    # print(timelisto)
    # print(ratelisto1)
    # for i in depths:
    #     x = []
    #     y = []
    #     for j in range(len(deptho)):
    #         if deptho[j] == i:
    #             x.append(timelisto[j])
    #             y.append(ratelisto1[j])
    #             print(i, deptho[j])
    #     plt.scatter(np.array(x)-min(x), y)
    #     plt.title('Depth = '+str(i))
    #     plt.savefig('C:\\Users\\lzvio\\Intensity vs Time Plots\\Depth'+str(i)+'.png')

    #Plot per level, subtract nearest background
    # for i in depths:
    #     x = []
    #     y = []
    #     for j in range(len(deptho)):
    #         if deptho[j] == i:
    #             stuff = abs(np.array(timelistc) - timelisto[j])
    #             index = stuff.argmin()
    #             # print(timelistc[index], timelisto[j])
    #             x.append(timelisto[j])
    #             y.append(ratelisto1[j] - ratelistc1[index])
    #     # print(i, x, y)
    #     plt.scatter(x, y)
    #     plt.ylim(0, 100)
    #     plt.title('Depth = '+str(i))
    #     plt.show()
    #     plt.savefig('C:\\Users\\lzvio\\Intensity vs Time Plots\\Depth'+str(i)+'-Background.png')
    #     x.clear()
    #     y.clear()

    # Plot all 128 rate from single day, minus background
    x = []
    y = []

    # xc = []
    # ytesto = []
    # ytestc = []

    for j in range(len(timelisto)):
        stuff = abs(np.array(timelistc) - timelisto[j])
        index = stuff.argmin()
        x.append(timelisto[j])
        y.append(ratelisto1[j] - ratelistc1[index])
        # print(i, x, y)

        # xc.append(timelistc[index])
        # ytesto.append(ratelisto1[j])
        # ytestc.append(ratelistc1[index])

    # x, xc, ytesto, ytestc = zip(*sorted(zip(x, xc, ytesto, ytestc)))
    # for i in range(len(ytesto)):
    #     print(x[i], ytesto[i], xc[i], ytestc[i])

    x = np.array(x)-min(x)

    plt.scatter(x, y)
    plt.ylim(0, 120)
    par, cov = scipy.optimize.curve_fit(exp, x, y, p0=[6.53*10**(-5), 1.04*10**(2), 1.24*10**(2)], maxfev=100000)
    plt.plot(x, exp(x, *par))
    plt.title('Month, Day='+str(dir[19:23])+', Par: '+str(par[0])+', '+str(round(par[1], 2))+', '+str(np.round(par[2], 2)))
    plt.show()
    print(par)

#     To plot begin/end from multiple days
#     x = []
#     y = []
#     for j in range(len(timelisto)):
#         stuff = abs(np.array(timelistc) - timelisto[j])
#         index = stuff.argmin()
#         x.append(timelisto[j])
#         y.append(ratelisto1[j] - ratelistc1[index])
#         # print(i, x, y)
#     x, y = zip(*sorted(zip(x, y)))
#     times.append(x[0])
#     times.append(list(x).pop())
#     rates.append(y[0])
#     rates.append(list(y).pop())
# times = []
# rates = []
#Call function here with each day's folder path
# times = np.array(times)
# times[2:4] = times[2:4]+24*3600
# times[4:6] = times[2:4]+24*3600*2
# times[6:8] = times[2:4]+24*3600*3
# plt.scatter(times, rates)
# plt.title('First and Last 128 nm Intensity Per Day')
# plt.show()

# function("C:\\Users\\lzvio\\20231005_measurement\\", 1280)
# function("C:\\Users\\lzvio\\20231006_measurement\\", 1280)
function("C:\\Users\\lzvio\\20231009_measurement\\", 1280)
# function("C:\\Users\\lzvio\\20231010_measurement\\", 1280)


# Day 1 Fit Parameters: [1.47938280e-04 1.48632302e+02 2.66501532e+02]
# Day 2 Fit Parameters: [3.93767742e-04 1.09954282e+02 2.32693275e+02]
# Day 3 Fit Parameters: [-1.76998555e-03 -5.67332915e-02  3.48789744e+01]