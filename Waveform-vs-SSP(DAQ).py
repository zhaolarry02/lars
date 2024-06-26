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

# Initial SSP Input Settings. See SSP Manual (https://indico.fnal.gov/event/12392/contributions/13933/attachments/9262/11900/docdb-1571.pdf) for more details.
I1 = 1000 # 'IntegratedSum' window
I2 = 200  # Baseline ('Prerise') window
M1 = 40   # 'PeakSum' sampling separation window
M2 = 20   # 'IntegratedSum' window portion to from initial bound to trigger point

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

pedestal_diff = [] # Prerise versus waveform baseline calculation
for i in range(num):
    pedestal_diff.append((np.sum(waveform[i][pretrig-M2-I2:pretrig-M2])) / (df['Prerise'][i]))
    # pedestal_diff.append((df['Baseline'][i]/4) / (df['Prerise'][i]/I2))

pedestal_sub_diff = []
for i in range(num):
    header1 = np.sum(waveform[i][pretrig-M2:pretrig-M2+I1]) - (np.sum(waveform[i][pretrig-M2-I2:pretrig-M2])*(I1/I2))
    header2 = df['IntegratedSum'][i] - (df['Prerise'][i]*(I1/I2))
    # header3 = np.sum(waveform[i][pretrig-M2:pretrig-M2+I1]) -  (df['Prerise'][i]*(I1/I2))
    # header4 = df['IntegratedSum'][i] - (np.sum(waveform[i][pretrig-M2-I2:pretrig-M2])*(I1/I2))

    header5 = df['PeakSum'][i] - (np.sum(waveform[i][pretrig-M2-I2:pretrig-M2])*(M1/I2))
    header6 = df['PeakSum'][i] - (df['Prerise'][i]*(M1/I2))
    # sspintbaseline = (df['IntegratedSum'][i] - df['Baseline'][i]/4*I1)

    pedestal_sub_diff.append((header1) / (header2))

waveform_pedestals = []
for i in range(num):
    waveform_pedestals.append(np.sum(waveform[i][pretrig-M2-I2:pretrig-M2]))
# print(np.mean(df['IntegratedSum'])-np.mean(waveform_pedestals)*(I1/I2))
# print(np.mean(df['IntegratedSum'])-np.mean(df['Prerise']*(I1/I2)))


plt.figure()
plt.hist(pedestal_diff, bins=np.linspace(-8, 4, 100), alpha=0.5)
plt.show()


# Plot SiPM Trigger Waveform Example
# x = range(2000)
# y = waveform[1]
# plt.plot(x, y)
# plt.title('SiPM Trigger Waveform')
# plt.xlabel('Time Ticks (6.667 ns)')
# plt.ylabel('ADC Counts')
# plt.show()
