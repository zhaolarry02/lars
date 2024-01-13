# Prints Trigger Number, Time Span, and Trigger Frequency Per Channel.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_closed = "C:\\Users\\lzvio\\OneDrive\\Desktop\\20230719_measure\\60tin_closed-0_2023-07-19_15-12-21.csv"
file = "C:\\Users\\lzvio\\OneDrive\\Desktop\\20230719_measure\\60tin_1240A3-0_2023-07-19_15-16-52.csv"
Wavelength = '1240A'

dfc = pd.read_csv(file_closed)
df = pd.read_csv(file)


def new_timestamps(df):
    # Create new time variables in seconds units
    freq=150000000. # 150 MHz
    df["SyncDelay_S"] = df['SyncDelay']/freq
    df["timestamp_S"] = (        df['IntTimestamp1'] + 
                         (2**16)*df['IntTimestamp2'] + 
                         (2**32)*df['IntTimestamp3'] ) / freq
new_timestamps(dfc)
new_timestamps(df)

# dfc.sort_values(by=['ChannelID'])
# df.sort_values(by=['ChannelID'])

# closed_freq = []
# freq = []
freq_diff = []
ch = [1, 2, 4, 5]

for i in ch:
    numc = len(dfc[dfc['ChannelID']==i])
    diffc = np.max(dfc["timestamp_S"][dfc['ChannelID']==i]) - np.min(dfc["timestamp_S"][dfc['ChannelID']==i])
    # closed_freq.append(numc/diffc)
    num = len(df[df['ChannelID']==i])
    diff = np.max(df["timestamp_S"][df['ChannelID']==i]) - np.min(df["timestamp_S"][df['ChannelID']==i])
    # freq.append(num/diff)
    freq_diff.append((num/diff)-(numc/diffc))

# print('Closed Trigger Frequency'+str(closed_freq))
# print('Open Trigger Frequency'+str(freq))
print('Trigger Frequency Difference'+str(freq_diff))


plt.bar(ch, freq_diff)
plt.title(Wavelength)
plt.xlabel('Channel')
plt.ylabel('Photon Detection Frequency (Hz)')
plt.show()
# plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\20230719_measure\\Plots\\Photon_Detection_Frequency_'+Wavelength+'.png', dpi=150)

'''
file_closed = "C:\\Users\\lzvio\\OneDrive\\Desktop\\LArS_Run1\\60tin_closed_2-0_2023-07-10_15-59-17.csv"

dfc = pd.read_csv(file_closed)

def closed_timestamps(dfc):
    # Create new time variables in seconds units
    freq=150000000. # 150 MHz
    dfc["SyncDelay_S"] = dfc['SyncDelay']/freq
    dfc["timestamp_S"] = (       dfc['IntTimestamp1'] + 
                         (2**16)*dfc['IntTimestamp2'] + 
                         (2**32)*dfc['IntTimestamp3'] ) / freq
closed_timestamps(dfc)
dfc.sort_values(by=['ChannelID'])
closed_freq = []
ch = [1, 2, 4, 5, 6, 7, 8]
for i in ch:
    num = len(dfc[dfc['ChannelID']==i])
    diff = np.max(dfc["timestamp_S"][dfc['ChannelID']==i]) - np.min(dfc["timestamp_S"][dfc['ChannelID']==i])
    closed_freq.append(num/diff)
'''
