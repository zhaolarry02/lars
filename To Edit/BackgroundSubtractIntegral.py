
# Plots Histogram of Background Subtracted Integral of Waveforms Per Channel

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("60tin_1240A-0_2023-07-10_11-52-22.csv")
df.sort_values(by=['ChannelID'])
data_files = ["60tin_1240A_Ch1-0_2023-07-10_11-52-22.dat", "60tin_1240A_Ch2-0_2023-07-10_11-52-22.dat", "60tin_1240A_Ch4-0_2023-07-10_11-52-22.dat", "60tin_1240A_Ch5-0_2023-07-10_11-52-22.dat", "60tin_1240A_Ch6-0_2023-07-10_11-52-22.dat", "60tin_1240A_Ch7-0_2023-07-10_11-52-22.dat", "60tin_1240A_Ch8-0_2023-07-10_11-52-22.dat"]
dfw = pd.concat((pd.read_csv(filename, header=None) for filename in data_files))
waveform = [dfw[0].iloc[i+24:i+2024] for i in range(0,len(dfw),2024)]

# plt.figure()
# plt.plot(range(len(waveform[6])), waveform[6])
# plt.show()

integral = []
for i in range(len(waveform)):
    integral.append()
df['Integral Above Baseline'] = integral

for i in [1, 2, 4, 5, 6, 7, 8]:
    if df['ChannelID'] == i:
        plt.figure()
        plt.hist(waveform[i], bins=25)
        plt.show()

plt.figure()
plt.hist(integral, bins=1000)
plt.xlim(-5000, 10000)
plt.show()
