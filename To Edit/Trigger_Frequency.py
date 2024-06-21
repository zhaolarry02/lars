# Plots Trigger Frequency minus Background versus Channel.

import numpy as np
import matplotlib.pyplot as plt
from Analysis import Analysis

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


ratediff("C:\\Users\\...\\20230719_measure\\", [1, 2, 4, 5], 60, '124')
