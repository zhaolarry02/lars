# Prints Trigger Number, Time Span, and Trigger Frequency Per Channel.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = ["C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\60tin_closed-0_2023-07-27_08-43-36.csv",
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
        "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\20tin_closed-0_2023-07-27_16-03-17.csv"]

Wavelength = 'Closed'

for j in file:
    df = pd.read_csv(j)
    indexEOF = df[ (df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    # Create new time variables in seconds units
    freq=150000000. # 150 MHz
    df["timestamp_S"] = (        df['IntTimestamp1'] + 
                         (2**16)*df['IntTimestamp2'] + 
                         (2**32)*df['IntTimestamp3'] ) / freq
    freq_list = []
    ch = [1, 2, 4, 5]
    for i in ch:
        num = len(df[df['ChannelID']==i])
        diff = np.max(df["timestamp_S"][df['ChannelID']==i]) - np.min(df["timestamp_S"][df['ChannelID']==i])
        freq_list.append(num/diff)
    print(str(j)+', '+str(freq_list))
