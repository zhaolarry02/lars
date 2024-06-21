import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from Analysis import Analysis


# Code Plots Trigger Rate per Channel For a Single Data File
def trigrateperchannelplot(file):
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



# Prints Shutter Closed Trigger Rates per Channel for Multiple Files
# dir is "C:\\Users\\lzvio\\OneDrive\\Desktop\\7.27"
def trigrateperchannelprint(dir, wvl): # wvl is string value e.g. 'clo', '128'
    channelID = [1, 2, 4, 5]
    ana = Analysis(1280)
    for filename in os.listdir(dir):
        t = re.split("_", filename) # Split file title
        if t[1][:3] == wvl:
            # time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8]) # Calculate time in seconds since time 00:00:00 of data collection date
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID) # Calculate Trigger Rate in Hertz via 'Analysis' script trigger rate function
            print(filename+': '+[trigrate[0], trigrate[1], trigrate[2], trigrate[3]])



# Print, Return Mean Trigger Rate per Channel
def trigratemeanoutput(dir, channelID, depth, wvl): # depth is value e.g. 60; wvl is string value e.g. 'clo', '128'
    trigratelist = []
    for filename in os.listdir(dir):
        t = re.split("_", filename) # Split file title
        if t[1][:3] == wvl  &  t[0][:2] == depth:
            df = ana.import_file(dir+filename, [])
            trigrate = ana.trig_rate(df, channelID) # Calculate Trigger Rate in Hertz via 'Analysis' script trigger rate function
            trigratelist.append(trigrate)
    rateperch = [np.mean([i[0] for i in trigratelist]), np.mean([i[1] for i in trigratelist]), np.mean([i[2] for i in trigratelist]), np.mean([i[3] for i in trigratelist])]
    print(wvl, 'Ch 1 Rate:', rateperch[0], ' Ch 2 Rate:', rateperch[1], ' Ch 4 Rate:', rateperch[2], ' Ch 5 Rate:', rateperch[3])
    return rateperch

# Plot Mean Trigger Rate minus Mean Background per Channel
def trigrateminusbkgd_vs_channel_plot(dir, channelID, depth, wvl): # here wvl is opened only e.g. '128' or '180', channelID is list e.g. [1, 2, 4, 5]
    closed = printtrigrate(dir, depth, 'clo')
    opened = printtrigrate(dir, depth, wvl)
    rateminusbkgd = []
    for i in range(len(channelID)):
        rateminusbkgd.append(opened[i] - closed[i])
    print(rateminusbkgd)

    plt.bar(channelID, rateminusbkgd)
    plt.title(str(depth)+'in. '+wvl+' Background Subtracted Rate vs SiPM Channel')
    plt.xlabel('SiPM Channel')
    plt.ylabel('Photon Detection Frequencyy (Hz)')
    plt.show()
    plt.savefig('C:\\Users\\lzvio\\...\\<name>+'.png', dpi=150)

trigrateminusbkgd_vs_channel_plot("C:\\Users\\...\\20230719_measure\\", [1, 2, 4, 5], 60, '124')
