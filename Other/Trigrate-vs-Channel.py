import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from Analysis import Analysis

# Code Plots Number of Triggers per Channel For a Single Wavelength

def triggerperchannel(file):
	ana = Analysis(1280)
	df = ana.import_file(file, [])
	counter = Counter(df['ChannelID'])
	trigrate = ana.trig_rate(df, channelID)
	plt.figure()
	# plt.scatter(counter.keys(), counter.values())
	plt.scatter(counter.keys(), trigrate)
	plt.title('Trigger Rate vs Channel')
	plt.xlabel('SiPM Channel')
	plt.ylabel('Trigger Number')
	plt.show()
