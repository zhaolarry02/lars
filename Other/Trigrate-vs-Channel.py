import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from Analysis import Analysis

# Code Plots Trigger Rate per Channel For a Single Data File
def trigrateperchannel(file):
        channelID = [1, 2, 4, 5]
        ana = Analysis(1280)
	df = ana.import_file(file, [])
	counter = Counter(df['ChannelID'])
	trigrate = ana.trig_rate(df, channelID)
	
	plt.figure()
	# plt.scatter(counter.keys(), counter.values()) # Plot of number of triggers per channel
	plt.scatter(counter.keys(), trigrate)
	plt.title('Trigger Rate vs Channel')
	plt.xlabel('SiPM Channels')
	plt.ylabel('Trigger Rate')
	plt.show()


# Prints Shutter Closed Trigger Rates per Channel
# dir is "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27"
def printtrigrateperchannel(dir):
    channelID = [1, 2, 4, 5]
    ana = Analysis(1280)
    for filename in os.listdir(dir):
        t = re.split("_", filename) # Split file title
        if t[1][:3] == 'clo':
            # time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8]) # Calculate time in seconds since time 00:00:00 of data collection date
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID) # Calculate Trigger Rate in Hertz via 'Analysis' script trigger rate function
            print(filename+': '+[trigrate[0], trigrate[1], trigrate[2], trigrate[3]])
