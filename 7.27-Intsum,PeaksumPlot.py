import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# time for rate calculation
def new_timestamps(df):
    # Create new time variables in seconds units
    freq=150000000. # 150 MHz
    df["SyncDelay_S"] = df['SyncDelay']/freq
    df["timestamp_S"] = (        df['IntTimestamp1'] + 
                         (2**16)*df['IntTimestamp2'] + 
                         (2**32)*df['IntTimestamp3'] ) / freq


# Closed Shutter:

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
Ch = 1

# Ch 1 Intsum: 235000 to 238000
# Ch 1 Peaksum: 15800 to 16500
# Ch 2 Intsum: 239000 to 242000
# Ch 2 Peaksum: 16000 to 16700

Depth = [127.22, 127.22, 101.83, 101.83, 101.83, 76.33, 76.33, 50.97, 50.97, 50.97, 50.97, 25.34, 25.34, 2.22, 2.22]
Run   = [0, 1, 0, 1, 2, 0, 1, 0, 1, 2, 3, 0, 1, 0, 1]

for j in [0]: # range(len(filec)):
    df = pd.read_csv(filec[j], low_memory=False)

    indexEOF = df[(df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    
    # IntegratedSum Plot
    plt.figure()
    plt.hist(df.loc[df['ChannelID'] == Ch]['IntegratedSum'].values, bins=range(235000, 238000, 20), density=True, alpha=1, label=str(Depth[j]))
    plt.title('7.27 '+str(Wavelength)+' Ch '+str(Ch)+' IntSum (Log, Raw, Normed) '+str(Depth[j])+'cm_'+str(Run[j]))
    plt.yscale("log")
    plt.ylim(0, 0.004)
    plt.grid()
    # plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\Plots\\IntSum\\7.27_'+str(Wavelength)+'_IntSum_log_Ch'+str(Ch)+'_'+str(Depth[j])+'cm_'+str(Run[j])+'.png', dpi=150)
    plt.show()

    # PeakSum Plot
    plt.figure()
    plt.hist(df.loc[df['ChannelID'] == Ch]['PeakSum'].values, bins=range(15800, 16500, 10), density=True, alpha=1, label=str(Depth[j]))
    plt.title('7.27 '+str(Wavelength)+' Ch '+str(Ch)+' PeakSum (Log, Raw, Normed) '+str(Depth[j])+'cm_'+str(Run[j]))
    plt.yscale("log")
    plt.ylim(0, 0.04)
    plt.grid()
    # plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\Plots\\PeakSum\\7.27_'+str(Wavelength)+'_PeakSum_log_Ch'+str(Ch)+'_'+str(Depth[j])+'cm_'+str(Run[j])+'.png', dpi=150)
    plt.show()

    ### > 2 PE Cuts:

    ## IntSum
    # plt.figure()
    # intsum = df.loc[df['ChannelID'] == Ch]['IntegratedSum'].values
    # intsum_cut = [i for i in intsum if i >= 239000]
    # plt.hist(intsum_cut, bins=range(239000, 242000, 20), density=True, alpha=1, label=str(Depth[j]))
    # plt.yscale("log")
    # plt.title('7.27 '+str(Wavelength)+' Ch '+str(Ch)+' IntSum (Log, Raw, Cut, Normed) '+str(Depth[j])+'cm_'+str(Run[j]))
    # plt.ylim(0, 0.004)
    # plt.grid()
    # # plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\Plots\\IntSum\\7.27_'+str(Wavelength)+'_IntSum_Cut_log_Ch'+str(Ch)+'_'+str(Depth[j])+'cm_'+str(Run[j])+'.png', dpi=150)
    # plt.show()

    # # PeakSum
    # plt.figure()
    # peaksum = df.loc[df['ChannelID'] == Ch]['PeakSum'].values
    # peaksum_cut = [i for i in peaksum if i >= 16250]
    # plt.hist(peaksum_cut, bins=range(16250,16800, 10), density=True, alpha=1, label=str(Depth[j]))
    # plt.yscale("log")
    # plt.title('7.27 '+str(Wavelength)+' Ch '+str(Ch)+' PeakSum (Log, Raw, Cut, Normed) '+str(Depth[j])+'cm_'+str(Run[j]))
    # plt.ylim(0, 0.04)
    # plt.grid()
    # # plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\Plots\\PeakSum\\7.27_'+str(Wavelength)+'_PeakSum_Cut_log_Ch'+str(Ch)+'_'+str(Depth[j])+'cm_'+str(Run[j])+'.png', dpi=150)
    # plt.show()


# 180 nm:
file1 = ["C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_1800A3-0_2023-07-27_09-29-12.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\50tin_1800A3-0_2023-07-27_11-02-50.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\40tin_1800A3-0_2023-07-27_12-59-43.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\30tin_1800A3-0_2023-07-27_14-39-09.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\20tin_1800A3-0_2023-07-27_15-35-04.csv",
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\11tin_1800A3-0_2023-07-27_17-46-32.csv"]

Wavelength = '180 nm'
Ch = 1
# Ch 1 Intsum Range: bins=range(235000, 238000, 20)
# Ch 1 PeakSum Range: bins=range(15700, 16400, 10)
# Ch 2 Intsum Range: bins=range(239000, 242000, 20)
# Ch 2 PeakSum Range: bins=range(16000, 16700, 10)

Depth = [127.22, 101.83, 76.33, 50.97, 25.34, 2.22]


for j in [0]: # range(len(file1)):
    df = pd.read_csv(file1[j], low_memory=False)

    indexEOF = df[(df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    
    # IntSum
    plt.figure()
    plt.hist(df.loc[df['ChannelID'] == Ch]['IntegratedSum'].values, bins=range(235000, 238000, 20), density=True, alpha=1, label=str(Depth[j]))
    plt.title('7.27 '+str(Wavelength)+' Ch '+str(Ch)+' IntSum (Log, Raw, Normalized) '+str(Depth[j])+'cm')
    plt.yscale("log")
    plt.ylim(0, 0.004)
    plt.grid()
    # plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\Plots\\IntSum\\7.27_'+str(Wavelength)+'_IntSum_log_Ch'+str(Ch)+'_'+str(Depth[j])+'cm.png', dpi=150)
    plt.show()
    
    # PeakSum
    plt.figure()
    plt.hist(df.loc[df['ChannelID'] == Ch]['PeakSum'].values, bins=range(15700, 16400, 10), density=True, alpha=1, label=str(Depth[j]))
    plt.title('7.27 '+str(Wavelength)+' Ch '+str(Ch)+' PeakSum (Log, Raw, Normalized) '+str(Depth[j])+'cm')
    plt.yscale("log")
    plt.ylim(0, 0.04)
    plt.grid()
    # plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\Plots\\PeakSum\\7.27_'+str(Wavelength)+'_PeakSum_log_Ch'+str(Ch)+'_'+str(Depth[j])+'cm.png', dpi=150)
    plt.show()
    



'''
# Code below plots all hist on the same figure
# 1. Simpler

# depth = [60, 50, 40, 30, 20]
for j in range(len(file)):
    df = pd.read_csv(file[j], low_memory=False)

    indexEOF = df[ (df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    plt.hist(df.loc[df['ChannelID'] == 1]['IntegratedSum'].values, bins=range(235000, 238000, 20), alpha=0.5, label=str(depth[j]))
    plt.legend(loc='upper right')
plt.show()

# 2. Complex
lists = [[] for i in range(5)]
counter = 0

for j in file:
    df = pd.read_csv(j, low_memory=False)

    indexEOF = df[ (df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    lists[counter].insert(0, df.loc[df['ChannelID'] == 1]['IntegratedSum'].values)
    counter += 1

for i in range(len(lists)):
    plt.hist(lists[i], bins=range(235000, 238000, 20), alpha=0.2, label=str(depth[i]))
    plt.legend(loc='upper right')
plt.show()

int_list = []
for j in file:
    df = pd.read_csv(j)
    int_list.append(np.mean(df.loc[df['ChannelID'] == 1]['IntegratedSum']))

    intsum = []
    intsum.append(df.loc[df['ChannelID'] == 1]['IntegratedSum'])

    plt.figure()
    plt.hist(intsum, alpha=0.5, label=j)
    plt.legend(bbox_to_anchor=(1.2, 1), loc='upper right')

    # Create new time variables in seconds units

    freq=150000000. # 150 MHz
    df["timestamp_S"] = (        df['IntTimestamp1'] + 
                         (2**16)*df['IntTimestamp2'] + 
                         (2**32)*df['IntTimestamp3'] ) / freq
    integral = []
    ch = [1, 2, 4, 5]
    for i in ch:
        integral.append([df['IntegratedSum'][i] - df['Prerise'][i]/I2*I1])
'''