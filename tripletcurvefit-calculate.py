import scipy.optimize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

data_files =  ["C:\\Users\\lzvio\\Lifetime\\Waveform_2046_Ch5-0_2023-10-04_16-02-56.dat"]
                # "C:\\Users\\lzvio\\Lifetime\\Waveform_2046_Ch1-0_2023-10-04_16-02-56.dat" #, Ch 1
                # "C:\\Users\\lzvio\\Lifetime\\Waveform_2046_Ch2-0_2023-10-04_16-02-56.dat" #Ch 2
                # "C:\\Users\\lzvio\\Lifetime\\Waveform_2046_Ch4-0_2023-10-04_16-02-56.dat", #Ch 4
                # "C:\\Users\\lzvio\\Lifetime\\Waveform_2046_Ch5-0_2023-10-04_16-02-56.dat", #Ch 5
                # "C:\\Users\\lzvio\\Lifetime\\Waveform_2046_Ch6-0_2023-10-04_16-02-56.dat"  #Ch 6
                
dfw = pd.concat((pd.read_csv(filename, header=None) for filename in data_files))

# num = dfw.shape[0]
waveform = np.array([dfw[0].iloc[i+24:i+2070] for i in range(0, (dfw.shape[0]//2070)*2070, 2070)])

meanwf = []

for i in range(2046):
    # stuff = list(np.array(waveform).T[i]) #loads but doesn't get right plot, slower than other numpy method
    # stuff = [item[i] for item in waveform]
    # stuff = list(zip(*waveform))[i]

    stuff = np.array(waveform)[:,i]
    meanwf.append(sum(stuff)/len(stuff))

meanwf = np.array(meanwf)
meanwf = meanwf.astype(str)

file = open("C:\\Users\\lzvio\\triplet_data5.txt", 'w')
for item in meanwf:
    file.write(item+"\n")
file.close()