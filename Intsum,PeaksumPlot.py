# Compares Our Calculated Baseline Subtracted Integral Sum with Header File IntegratedSum
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from Analysis import Analysis

# channelID = [1, 2, 4, 5]
depth = [60, 55, 50, 45, 40, 35, 30, 26, 25, 21, 17, 14, 12]
depthcm = [128.0970994, 114.9495949, 102.4368448, 89.3539062, 76.68776733, 64.50960174, 51.8504376, 42.32291091, 39.6549546, 27.42838632, 17.6438245, 9.824104101, 4.674364388]
wavelength = [124, 125, 126, 127, 128, 129, 130, 131, 132, 142, 152, 173, 174, 175, 176, 177, 178, 179, 180]
wv = 128
ana = Analysis(1280)


for level in depth:
	data_files = []
	for filename in os.listdir("C:\\Users\\lzvio\\1107-1111Data"): 
		t = re.split("_", filename)
		if t[1][:3] == 'clo' and float(t[0][:2]) == level:
			data_files.append(filename)
	df = pd.concat((pd.read_csv("C:\\Users\\lzvio\\1107-1111Data\\"+filename, skiprows=[1]) for filename in data_files));
	intsum  = df.loc[df['ChannelID'] == 1]['IntegratedSum'].values
	peaksum = df.loc[df['ChannelID'] == 1]['PeakSum'].values
	prerise = df.loc[df['ChannelID'] == 1]['Prerise'].values

	plt.figure()
	plt.title(str(level)+'in LAr Ch 1 Background IntSum Histogram')
	plt.hist(intsum, bins=range(235500, 238000, 50), alpha=0.5)
	plt.xlabel('Integrated Sum')
	plt.grid()
	plt.savefig('C:\\Users\\lzvio\\BackgroundIntSum,PeaksumvDepth\\Intsum_'+str(level)+'in_Closed_Ch1.png')
	# plt.show()

	plt.figure()
	plt.title(str(level)+'in LAr Ch 1 Background PeakSum Histogram')
	plt.hist(peaksum, bins=range(15700, 16400, 10), alpha=0.5)
	plt.xlabel('Integrated Sum')
	plt.grid()
	plt.savefig('C:\\Users\\lzvio\\BackgroundIntSum,PeaksumvDepth\\Peaksum_'+str(level)+'in_Closed_Ch1.png')
	# plt.show()