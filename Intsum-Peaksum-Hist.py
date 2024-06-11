# Plot Intsum, Peaksum histograms for single wavelength / for background, at each depth

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from Analysis import Analysis

def intsumhist(path, wvl, ch):  # path to 1107-1111Data, wvl is string e.g. 'clo' or '128'
	depth = [60, 55, 50, 45, 40, 35, 30, 26, 25, 21, 17, 14, 12] # in inches
	ana = Analysis(1280)

	for level in depth:
		data_files = []
		for filename in os.listdir(path): 
			t = re.split("_", filename)
			if t[1][:3] == wvl and float(t[0][:2]) == level:
				data_files.append(filename)
		df = pd.concat((pd.read_csv(path+"\\"+filename, skiprows=[1]) for filename in data_files));
		intsum  = df.loc[df['ChannelID'] == ch]['IntegratedSum'].values
		prerise = df.loc[df['ChannelID'] == ch]['Prerise'].values

		plt.figure()
		plt.title(str(level)+'in LAr Ch '+str(ch)+' Shutter Closed IntSum Histogram')
		plt.hist(intsum, bins=range(235500, 238000, 50), alpha=0.5)
		plt.xlabel('Integrated Sum')
		plt.grid()
		plt.savefig('C:\\...\\Intsum_'+str(level)+'in_Closed_Ch'+str(ch)+'.png')
		# plt.show()


def peaksumhist(path, wvl, ch):  # path to 1107-1111Data, wvl is string e.g. 'clo' or '128'
	depth = [60, 55, 50, 45, 40, 35, 30, 26, 25, 21, 17, 14, 12] # in inches
	ana = Analysis(1280)

	for level in depth:
		data_files = []
		for filename in os.listdir(path): 
			t = re.split("_", filename)
			if t[1][:3] == wvl and float(t[0][:2]) == level:
				data_files.append(filename)
		df = pd.concat((pd.read_csv(path+"\\"+filename, skiprows=[1]) for filename in data_files));
		peaksum = df.loc[df['ChannelID'] == ch]['PeakSum'].values
		prerise = df.loc[df['ChannelID'] == ch]['Prerise'].values

		plt.figure()
		plt.title(str(level)+'in LAr Ch '+str(ch)+' Shutter Closed PeakSum Histogram')
		plt.hist(peaksum, bins=range(15700, 16400, 10), alpha=0.5)
		plt.xlabel('Peak Sum')
		plt.grid()
		plt.savefig('C:\\...\\Peaksum_'+str(level)+'in_Closed_Ch'+str(ch)+'.png')
		# plt.show()


intsumhist("C:\\...\\1107-1111Data", wvl, 1) # wvl examples: 'clo', '128'
