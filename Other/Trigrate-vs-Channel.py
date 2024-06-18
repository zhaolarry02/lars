import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from Analysis import Analysis

# Code Plots Trigger Number or Rate per Channel For a Single Wavelength

def triggerperchannel(file):
	ana = Analysis(1280)
	df = pd.read_csv(file)
	df = ana.import_file(dir+filename, [])
	counter = Counter(df['ChannelID'])
  trigrate = ana.trig_rate(df, channelID)
	plt.figure()
	# plt.scatter(counter.keys(), counter.values())
	plt.scatter(counter.keys(), trigrate)
	plt.title('Trigger Rate vs Channel')
	plt.xlabel('SiPM Channel')
	plt.ylabel('Trigger Number')
	plt.show()
