import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# time function for rate calculation
def new_timestamps(df):
    # Create new time variables in seconds units
    freq=150000000. # 150 MHz
    df["SyncDelay_S"] = df['SyncDelay']/freq
    df["timestamp_S"] = (        df['IntTimestamp1'] + 
                         (2**16)*df['IntTimestamp2'] + 
                         (2**32)*df['IntTimestamp3'] ) / freq

'''
# Closed shutter:
print('Closed')
filec = ["C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_closed-0_2023-07-27_08-43-36.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_closed-0_2023-07-27_09-29-51.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\50tin_closed-0_2023-07-27_10-55-59.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\50tin_closed-1_2023-07-27_10-59-19.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\50tin_closed-0_2023-07-27_11-37-19.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\40tin_closed-0_2023-07-27_12-23-06.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\40tin_closed-0_2023-07-27_13-00-22.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\30tin_closed-0_2023-07-27_13-49-57.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\30tin_closed-0_2023-07-27_13-58-34.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\30tin_closed-0_2023-07-27_14-27-46.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\30tin_closed-0_2023-07-27_14-39-43.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\20tin_closed-0_2023-07-27_15-30-29.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\20tin_closed-0_2023-07-27_16-03-17.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_closed-0_2023-07-27_16-53-40.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_closed-0_2023-07-27_17-47-18.csv"]

Wavelength = 'Closed'

Ch = 2
# Ch 1: (df['PeakSum'] >= 16250) & (df['PeakSum'] <= 16450)
# Ch 2: (df['PeakSum'] >= 16450) & (df['PeakSum'] <= 16650)

Depth = [127.22, 127.22, 101.83, 101.83, 101.83, 76.33, 76.33, 50.97, 50.97, 50.97, 50.97, 25.34, 25.34, 2.22, 2.22]
Run   = [0, 1, 0, 1, 2, 0, 1, 0, 1, 2, 3, 0, 1, 0, 1]

for j in range(len(filec)):
    df = pd.read_csv(filec[j], low_memory=False)
    indexEOF = df[(df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    new_timestamps(df)

    # rate calculation
    peaksum2 = df.loc[(df['ChannelID'] == Ch) & (df['PeakSum'] >= 16450) & (df['PeakSum'] <= 16650)]
    rate = len(peaksum2) / (np.max(df['timestamp_S']) - np.min(df['timestamp_S']))
    print(rate)


# 180 nm:
print('Open')
file1 = ["C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1800A3-0_2023-07-27_09-29-12.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\50tin_1800A3-0_2023-07-27_11-02-50.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\40tin_1800A3-0_2023-07-27_12-59-43.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\30tin_1800A3-0_2023-07-27_14-39-09.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\20tin_1800A3-0_2023-07-27_15-35-04.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1800A3-0_2023-07-27_17-46-32.csv"]

Wavelength = '180 nm'

Depth = [127.22, 101.83, 76.33, 50.97, 25.34, 2.22]

for j in range(len(file1)):
    df = pd.read_csv(file1[j], low_memory=False)
    indexEOF = df[(df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    new_timestamps(df)

    # rate calculation
    peaksum2 = df.loc[(df['ChannelID'] == Ch) & (df['PeakSum'] >= 16450) & (df['PeakSum'] <= 16650)]
    rate = len(peaksum2) / (np.max(df['timestamp_S']) - np.min(df['timestamp_S']))
    print(rate)
'''

# 60 in. All Wavelength:

'''
file = ["C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_closed-0_2023-07-27_08-43-36.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1240A3-0_2023-07-27_08-49-32.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1250A3-0_2023-07-27_08-52-28.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1260A3-0_2023-07-27_08-55-35.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1270A3-0_2023-07-27_08-58-53.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1280A3-0_2023-07-27_09-01-43.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1290A3-0_2023-07-27_09-05-08.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1300A3-0_2023-07-27_09-07-41.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1310A3-0_2023-07-27_09-10-04.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1320A3-0_2023-07-27_09-12-06.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1420A3-0_2023-07-27_09-14-24.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1500A3-0_2023-07-27_09-16-02.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1650A3-0_2023-07-27_09-17-31.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1730A3-0_2023-07-27_09-20-07.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1740A3-0_2023-07-27_09-21-59.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1750A3-0_2023-07-27_09-23-19.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1760A3-0_2023-07-27_09-24-56.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1770A3-0_2023-07-27_09-26-02.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1780A3-0_2023-07-27_09-27-09.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1790A3-0_2023-07-27_09-28-08.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1800A3-0_2023-07-27_09-29-12.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_closed-0_2023-07-27_09-29-51.csv"]
'''

'''
Single Level Wavelength Range 3PE Calculation:
Ch = 1
# Ch 1: range(16210, 16450, 10)
# Ch 2: range(16500, 16620, 10)
for j in range(len(file)): # [0, 1, 2, 3, 4, 5]: #
    df = pd.read_csv(file[j], low_memory=False)
    indexEOF = df[(df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    new_timestamps(df)

    # 3PE Rate Calculation
    num = len(df.loc[(df['ChannelID'] == Ch) & (df['PeakSum'] >= 16210) & (df['PeakSum'] <= 16450)])
    rate = num / (np.max(df['timestamp_S']) - np.min(df['timestamp_S']))
    print(rate)

    # PeakSum plot for 3PE range identification
    plt.hist(df.loc[df['ChannelID'] == Ch]['PeakSum'].values, bins=range(15500, 17000, 10), density=True, alpha=0.5)
    plt.hist(df.loc[(df['ChannelID'] == Ch) & (df['PeakSum'] >= 16210) & (df['PeakSum'] <= 16450)]['PeakSum'].values, bins=range(15700, 16700, 10), density=True, color = 'r', alpha=0.5)
    plt.yscale("log")
    plt.show()
'''

file = ["C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_closed-0_2023-07-27_16-53-40.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1240A3-0_2023-07-27_17-07-55.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1250A3-0_2023-07-27_17-10-47.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1260A3-0_2023-07-27_17-13-59.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1270A3-0_2023-07-27_17-20-45.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1280A3-0_2023-07-27_17-23-51.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1290A3-0_2023-07-27_17-26-28.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1300A3-0_2023-07-27_17-28-46.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1310A3-0_2023-07-27_17-30-52.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1320A3-0_2023-07-27_17-32-47.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1420A3-0_2023-07-27_17-34-35.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1500A3-0_2023-07-27_17-35-38.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1500A3-1_2023-07-27_17-36-10.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1650A3-0_2023-07-27_17-37-18.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1730A3-0_2023-07-27_17-38-38.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1740A3-0_2023-07-27_17-39-53.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1750A3-0_2023-07-27_17-41-07.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1760A3-0_2023-07-27_17-42-15.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1770A3-0_2023-07-27_17-43-25.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1780A3-0_2023-07-27_17-44-29.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1790A3-0_2023-07-27_17-45-28.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1800A3-0_2023-07-27_17-46-32.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_closed-0_2023-07-27_17-47-18.csv"]

# Frequency vs Wavelength Plot:
Ch = 1
wavelengths = ['Closed 0', '124', '125', '126', '127', '128', '129', '130', '131', '132', '142', '150', '150', '165', '173', '174', '175', '176', '177', '178', '179', '180', 'Closed 1']
rate_list = []
for j in range(len(file)):
    df = pd.read_csv(file[j], low_memory=False)
    indexEOF = df[(df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    new_timestamps(df)

    # Rate Calculation
    num = len(df.loc[(df['ChannelID'] == Ch)])
    rate = num / (np.max(df['timestamp_S']) - np.min(df['timestamp_S']))
    rate_list.append(rate)

plt.title('11 in Channel '+str(Ch)+' Frequency vs Wavelength')
plt.xlabel('Wavelengths (nm)')
plt.ylabel('Frequency (Hz)')
plt.bar(wavelengths, rate_list)
plt.xticks(rotation = 90)
plt.show()
