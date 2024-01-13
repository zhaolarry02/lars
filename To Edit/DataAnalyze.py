# plots histogram of baseline subtracted integral

import pandas as pd
import matplotlib.pyplot as plt

def import_file(header, I1):
    df = pd.read_csv(header)
    
    #delete the "FILE END" row
    indexEOF = df[(df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)

    integral = []

    for i in range(df.shape[0]):
        integral.append(df['IntegratedSum'][i] - df['Info.mean'][i]*I1)

    df['Integral'] = integral

    wavelength = 'Closed'

    for id in [1, 2, 4, 5]:
        plt.figure()
        plt.hist(df.loc[df['ChannelID'] == id, 'IntegratedSum'], bins=range(0, 3000, 40))
        plt.title(wavelength+' Channel'+str(id))
        plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\20230719_measure\\Plots\\IntegralSum'+wavelength+'Channel-'+str(id)+'.png', dpi=150)

        plt.figure()
        plt.hist(df.loc[df['ChannelID'] == id, 'Integral'], bins=range(0, 2000, 40))
        plt.title(wavelength+' Channel'+str(id))
        plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\20230719_measure\\Plots\\IntegralSum_NoPedestal'+wavelength+'Channel-'+str(id)+'.png', dpi=150)

        plt.figure()
        plt.hist(df.loc[df['ChannelID'] == id, 'PeakSum'], bins=range(0, 2000, 40))
        plt.title(wavelength+' Channel'+str(id))
        plt.savefig('C:\\Users\\lzvio\\OneDrive\\Desktop\\20230719_measure\\Plots\\IntegralSum'+wavelength+'Channel-'+str(id)+'.png', dpi=150)

# import_file("C:\\Users\\lzvio\\OneDrive\\Desktop\\7.17\\60tin_1500A3-0_2023-07-17_13-44-14.csv", 250)
