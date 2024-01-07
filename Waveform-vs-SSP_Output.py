# Compares the pedestal subtracted integral calculated from waveform values to the SiPM Signal Processor (SSP)'s processed 'IntegratedSum' (Integral bound begins M2 values before trigger, length of I1)
# Code for confirmation of SSP accuracy in calculations of Waveform Integral, Mean, and Pedestal.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:\\...\\60tin_1790A-2_2023-07-14_14-10-02.csv") # SSP output file
df.sort_values(by=['ChannelID'])

data_files =  [ "C:\\...\\60tin_1790A_Ch1-2_2023-07-14_14-10-02.dat",
                "C:\\...\\60tin_1790A_Ch2-2_2023-07-14_14-10-02.dat", 
                "C:\\...\\60tin_1790A_Ch4-2_2023-07-14_14-10-02.dat", 
                "C:\\...\\60tin_1790A_Ch5-2_2023-07-14_14-10-02.dat", 
                "C:\\...\\60tin_1790A_Ch6-2_2023-07-14_14-10-02.dat", 
                "C:\\...\\60tin_1790A_Ch8-2_2023-07-14_14-10-02.dat"] # Waveforms files (list of values constituting waveforms)
dfw = pd.concat((pd.read_csv(filename, header=None) for filename in data_files))
waveform = [dfw[0].iloc[i+24:i+2024] for i in range(0,len(dfw),2024)] # Waveforms files as list containing sublists. Each sublist contains values for one waveform.

num = df[df['ChannelID']==1]['ChannelID'].count()

# Initial SSP Input Settings
I1 = 1000 # Length of 'IntegratedSum' bounds
I2 = 200
M1 = 40
M2 = 20 # Length of position of 'IntegratedSum' initial bound preceding the trigger

pretrig = 400 # Number of saved values preceding the trigger
length = 2000 # Number of waveform values

mean_diff = [] # Info.mean versus waveform mean
for i in range(num):
    mean = np.mean(waveform[i])
    meandiff = mean / df['Info.mean'][i]
    mean_diff.append(meandiff)

int_diff = [] # IntegratedSum versus waveform integral calculation
for i in range(num):
    int_sum = np.sum(waveform[i][pretrig-M2:pretrig-M2+I1])
    intdiff = int_sum / df['IntegratedSum'][i]
    int_diff.append(intdiff)

peak_diff = [] # PeakSum versus waveform peaksum calculation
for i in range(num):
    peak_sum = np.sum(waveform[i][pretrig:pretrig+M1])
    peakdiff = peak_sum / df['PeakSum'][i]
    peak_diff.append(peakdiff)

pedestal_diff = []
for i in range(num):
    pedestal_diff.append((np.mean(waveform[i][:pretrig-M2])) / (df['Prerise'][i]/I2))
        # pedestal_diff.append((df['Baseline'][i]/4) / (df['Prerise'][i]/I2))

pedestal_sub_diff = []
int_sub_diff = []
for i in range(num):
    header1 = df['IntegratedSum'][i] - (df['Prerise'][i]/I2*I1)
    header2 = df['IntegratedSum'][i] - (np.mean(waveform[i][:pretrig-M2])*I1)
    pedestal_sub_diff.append((header2) / (header1))

    sspintprerise = (df['IntegratedSum'][i] - (df['Prerise'][i]/I2*I1))
    sspintbaseline = (df['IntegratedSum'][i] - df['Baseline'][i]/4*I1)
    intsubdiff = sspintprerise / header2
    int_sub_diff.append(intsubdiff)

plt.figure()
plt.title('I1=1000, I2=200, M1=40, M2=20')
plt.hist(pedestal_sub_diff, bins=np.linspace(0, 10, 50), alpha=0.5)
plt.show()

# Plot SiPM Trigger Waveform Example
x = range(2000)
y = waveform[600]
plt.plot(x, y)
plt.title('SiPM Trigger Waveform')
plt.xlabel('Time Ticks (6.667 ns)')
plt.ylabel('ADC Counts')
plt.show()
