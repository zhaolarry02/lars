import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from Analysis import Analysis # Use functions defined in 'Analysis' python script written by Dr. Mu Wei, Dr. Alex Himmel, and Larry Zhao

ana = Analysis(1280)
Ch = 1
# Ch 1 3PE bounds: (df['PeakSum'] >= 16250) & (df['PeakSum'] <= 16450)
# Ch 2 3PE bounds: (df['PeakSum'] >= 16450) & (df['PeakSum'] <= 16650)

# PeakSum plot for 3PE bin boundary identification
def find3PElimits(path):
    lowlim = 16210
    uplim = 16450
    for filename in os.listdir(path):
        df = ana.import_file(path+filename, [])
        plt.title(filename)
        plt.hist(df.loc[df['ChannelID'] == Ch]['PeakSum'].values, bins=range(15500, 17000, 10), density=True, alpha=0.5)
        plt.hist(df.loc[(df['ChannelID'] == Ch) & (df['PeakSum'] >= lowlim) & (df['PeakSum'] <= uplim)]['PeakSum'].values, bins=range(15700, 16700, 10), density=True, color = 'r', alpha=0.5)
        plt.yscale("log")
        plt.show()


# 3 PE Rate Calculation
def frequency3PE(path, filename, lowlim, uplim): # path and filename passed from function call; find lowlim and uplim using find3PElimits(path) 
    df = ana.import_file(path+filename, [])
    ana.new_timestamps(df)
        
    peaksum3pe = df.loc[(df['ChannelID'] == Ch) & (df['PeakSum'] >= lowlim) & (df['PeakSum'] <= uplim)]
    rate = len(peaksum3pe) / (np.max(df['timestamp_S']) - np.min(df['timestamp_S']))
    return rate


# Shutter Closed 3 PE Rate
def closed3PErate(path): # path to 7.27 data directory
    lowlim = 16250
    uplim = 16450
    print('Shutter Closed 3 PE Rate')
    for filename in os.listdir(path):
        t = re.split("_", filename) # Split file title
        if t[1][:3] == 'clo':
            rate = frequency3PE(path, filename, lowlim, uplim)
            print(filename, ' Frequency: ', round(rate, 5), '(Hz)')


# 180 nm 3 PE Rate
def open180nm3PErate(path): # path to 7.27 data directory
    lowlim = 16250
    uplim = 16450
    print('180 nm 3 PE Rate')
    for filename in os.listdir(path):
        t = re.split("_", filename) # Split file title
        if t[1][:3] == '180':
            rate = frequency3PE(path, filename, lowlim, uplim)
            print(filename, ' Frequency: ', round(rate, 5), '(Hz)')


# Single Depth Wavelength Range 3PE Rate
def LArDepth3PErate(path, depth): # path is to 7.27 data directory, depth is "<num>tin"
    lowlim = 16210
    uplim = 16450
    print('60in 3 PE Rate')
    for filename in os.listdir(path):
        t = re.split("_", filename) # Split file title
        if t[0][:5] == depth:
            rate = frequency3PE(path, filename, lowlim, uplim)
            print(filename, ' Frequency: ', round(rate, 5), '(Hz)')


# Single Depth **3 PE** Frequency vs Wavelength Plot:
def LArDepth3PEFreqWVPlot(path, depth): # path is to 7.27 data directory, depth is "<num>tin"
    lowlim = 16210
    uplim = 16450
    wavelengths = []
    rate_list = []
    for filename in os.listdir(path):
        t = re.split("_", filename) # Split file title
        if t[0][:5] == depth:
            wavelengths.append(t[1][:3])
            rate = frequency3PE(path, filename, lowlim, uplim)
            rate_list.append(rate)

    plt.title(depth+' Ch'+str(Ch)+' 3 PE Frequency vs Wavelength Plot')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Frequency (Hz)')
    plt.bar(wavelengths, rate_list)
    plt.xticks(rotation = 90)
    plt.show()


# Single Depth Frequency vs Wavelength Plot:
def LArDepthFreqWVPlot(path, depth): # path is to 7.27 data directory, depth is "<num>tin"
    wavelengths = []
    rate_list = []
    for filename in os.listdir(path):
        t = re.split("_", filename) # Split file title
        if t[0][:5] == depth:
            wavelengths.append(t[1][:3])

            df = ana.import_file(path+filename, [])
            ana.new_timestamps(df)
                
            num = len(df.loc[(df['ChannelID'] == Ch)])
            rate = num / (np.max(df['timestamp_S']) - np.min(df['timestamp_S']))
            rate_list.append(rate)

    plt.title(depth+' Ch'+str(Ch)+' Frequency vs Wavelength Plot')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Frequency (Hz)')
    plt.bar(wavelengths, rate_list)
    plt.xticks(rotation = 90)
    plt.show()


LArDepthFreqWVPlot("C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27\\", '11tin')
