import os
import numpy as np
import re
from datetime import datetime
from Analysis import Analysis
import matplotlib.pyplot as plt

def function(dir, wlen):
    timelistc = []
    ratelistc4 = []

    timelisto = []
    ratelisto4 = []

    channelID = [1, 2, 4, 5, 6]

    for filename in os.listdir(dir):
        # Finds time in seconds from first timestamp

        # filename = "Test"+"_"+Wavelength+"-"+Run+"_2023-10-03"+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        # match = re.search(r'\d{2}-\d{2}-\d{2}', filename)
        # date = datetime.strptime(match.group(), '%H:%M:%S').date()

        t = re.split("_", filename)

        if t[1][:6] == 'closed':
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timelistc.append(time)

            # date_object = datetime.strptime(t[2][2:10]+' '+t[3][:8], "%y-%m-%d %H-%M-%S")
            # timelistc.append(date_object)

            # Finds Trigger Rate
            ana = Analysis(wlen)
            df = ana.import_file("C:/Users/lzvio/Excel/"+filename, [])
            ratelistc4.append(ana.trig_rate(df, channelID)[2])
    
        else:
            time = (int(t[3][0:2]))*3600 + int(t[3][3:5])*60 + int(t[3][6:8])
            timelisto.append(time)

            # Finds Trigger Rate
            ana = Analysis(wlen)
            df = ana.import_file("C:/Users/lzvio/Excel/"+filename, [])
            ratelisto4.append(ana.trig_rate(df, channelID)[2])

    
    time_newc = np.array(timelistc) - min(timelistc)
    # print(time_newc)
    # print(ratelistc)
    plt.scatter(time_newc, ratelistc4, c='b', label='Ch 4')
    plt.legend()
    plt.title('Closed')
    plt.xlabel('Time (s)')
    plt.ylabel('Trigger Rate (Hz)')
    plt.ylim(0, 150)
    plt.grid()
    plt.show()
    
    time_newo = np.array(timelisto) - min(timelisto)
    # print(time_newo)
    # print(ratelisto)
    plt.scatter(time_newo, ratelisto4, c='b', label='Ch 4')
    plt.legend()
    plt.title('Open')
    plt.xlabel('Time (s)')
    plt.ylabel('Trigger Rate (Hz)')
    plt.ylim(0, 200)
    plt.grid()
    plt.show()
    
function("C:/Users/lzvio/Excel", 1280)