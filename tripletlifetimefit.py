import scipy.optimize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


def exp(x, m, a, b):
    return (a * np.exp(np.array([-i for i in x]) * m) + b)


def triplifetimedata(file, readoutwindow):                    
    dfw = pd.concat((pd.read_csv(filename, header=None) for filename in file))

    waveform = np.array([dfw[0].iloc[i+24:i+readoutwindow+24] for i in range(0, (dfw.shape[0]//(readoutwindow+24))*(readoutwindow+24), (readoutwindow+24))])

    meanwf = []

    for i in range(readoutwindow):
        wfpoint = np.array(waveform)[:,i]
        meanwf.append(np.mean(wfpoint))

    meanwfarray = np.array(meanwf)

    # meanwfstr = meanwfarray.astype(str)
    # file = open("C:\\...\\triplet_waveform.txt", 'w') # Create empty file in local directory
    # for value in meanwfstr:
    #     file.write(value+"\n")
    # file.close()

    return meanwfarray


def triplifetimeplot(file, readoutwindow):
    # # calling triplifetimedata requires time to compile. alternatively, uncomment the 5 lines in triplifetimedata for reading values to a txt file, change return to meanwfstr, uncomment these 4 lines below, and comment the triplifetimedata call below. 
    # f = open(file, "r")
    # data = f.read()
    # d = data.split('\n', )
    # f.close()
    # y = [float(i) for i in d]


    y = triplifetimedata(file, readoutwindow)
  

    x = range(0, readoutwindow)
    y = np.array([j-1510 for j in y]) # Could swap value 1510 for np.min(y), but np.min(y) plots less clear graph due to log scaling down to 0

    plt.plot(x, y, label='Mean Waveform minus Pedestal');
    plt.yscale("log")

    par, cov = scipy.optimize.curve_fit(exp, x[600:1300], y[600:1300], p0=[0.00475215556, 6.06369377*10**2, 0.823153580], maxfev=100000)
    plt.plot(x[600:1300], exp(x[600:1300], *par), label='Curve Fit, Lifetime = '+str(round(1/par[0]*6.6667, 2))+' ns')
    plt.yscale("log")

    plt.title('Triplet Lifetime')
    plt.xlabel('SSP Time Tick (6.667 ns / Tick)')
    plt.ylabel('Waveform Signal minus Pedestal')
    plt.legend()
    plt.show()

    print(par, 'Triplet Lifetime=', 1/par[0]*6.6667)


triplifetimeplot(["C:\\...\\Waveform_2046_Ch1-0_2023-10-04_16-02-56.dat"], 2046) # file is .dat file for a channel, readoutwindow is value up to 2046


# # Data Files:
#  ["C:\\...\\Waveform_2046_Ch1-0_2023-10-04_16-02-56.dat"]  # Ch 1
#  ["C:\\...\\Waveform_2046_Ch2-0_2023-10-04_16-02-56.dat"]  # Ch 2
#  ["C:\\...\\Waveform_2046_Ch4-0_2023-10-04_16-02-56.dat"]  # Ch 4
#  ["C:\\...\\Waveform_2046_Ch5-0_2023-10-04_16-02-56.dat"]  # Ch 5
#  ["C:\\...\\Waveform_2046_Ch6-0_2023-10-04_16-02-56.dat"]  # Ch 6


# # Triplet Lifetime Results:
# Ch 1: 1402.879 ns
# Ch 4: 1398.364 ns
# Ch 5: 1407.842 ns
# Ch 6: 1657.21  ns
