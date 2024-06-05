# Code written by Dr. Mu Wei

import os
import sys
import time
import argparse
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('classic')

from collections import Counter
from scipy.optimize import curve_fit


i1 = 1000
i2 = 200
m1 = 40
m2 = 20

class Analysis(object):
  def __init__(self, lwleng, wlength=2000, wpretrigger=300, offset=24):
      self.lwleng       = lwleng       # wavelength of light
      self.wlength      = wlength      # length of the waveform window
      self.wpretrigger  = wpretrigger  # length of the pretrigger window
      self.offset       = offset

  def import_file(self, header, data_files):
    print('Importing data...')
    tstart = time.time()
    
    #load header files
    df = pd.read_csv(header, low_memory=False)
    
    #calculate the trigger time
    self.new_timestamps(df)
    
    #delete the "FILE END" row
    indexEOF = df[ (df['Event'] == 'FILE END')].index
    df.drop(indexEOF, inplace=True)
    
    df.sort_values(by=['ChannelID'])
    
    if len(data_files) > 0:
        #load raw waveform files
        dfw = pd.concat((pd.read_csv(filename, header=None) for filename in data_files))
    
        rawWaveform = np.array([dfw[0].iloc[i+self.offset:i+self.offset+self.wlength] for i in range(0, len(dfw), self.wlength+self.offset)])
        
        baseline    = self.baseline_sum(rawWaveform)
        peak        = self.peak_sum(rawWaveform)
        integral    = self.integral_sum(rawWaveform)
        
        pedestal    = self.pedestal_finding(rawWaveform)
        recWaveform = self.rec_waveform(rawWaveform, pedestal)

        #df['WaveBase'] = baseline
        #df['WaveInt']  = integral
        #df['WavePeak'] = peak
        #df['Pedestal'] = pedestal
        print('Data have been imported and processed in '+str(time.time()-tstart)+'s.')
        return df, rawWaveform, recWaveform
    
    print('Data have been imported and processed in '+str(time.time()-tstart)+'s.')
    return df
    
  def new_timestamps(self, df):
      # Create new time variables in seconds units
      freq=150000000. # 150 MHz
      df["SyncDelay_S"] = df['SyncDelay']/freq
      df["timestamp_S"] = (        df['IntTimestamp1'] + 
                           (2**16)*df['IntTimestamp2'] + 
                           (2**32)*df['IntTimestamp3'] ) / freq
  
  def pedestal_finding(self, rawWaveform):
      pedestal = rawWaveform[:,0:self.wpretrigger-10]
      
      pmean = np.mean(pedestal, axis=1)
      pstd  = np.std(pedestal, axis=1)
      pupper = pmean + pstd*3
      enum = pedestal.shape[0]
      for i in range(0, enum):
          #exclude the small peaks in the pretrigger window
          pedestal[i][pedestal[i]>pupper[i]] = pmean[i]
          
      pedestal = np.mean(pedestal, axis=1)
      return pedestal
      
  def rec_waveform(self, rawWaveform, pedestal):
      enum = pedestal.shape[0]
      for i in range(0, enum):
          rawWaveform[i] = rawWaveform[i] - pedestal[i]
          
      #avoid negative value in the recWaveform
      recWaveform = np.maximum(rawWaveform, 0.0)
      return recWaveform

  def baseline_sum(self, rawWaveform):
      baseline = []
      for i in range(len(rawWaveform)):
         baseline.append(np.sum(np.array(rawWaveform[i][self.wpretrigger-m2-i2:self.wpretrigger-m2]))/i2)
      baseline = np.array(baseline)
      return baseline
      
  def integral_sum(self, rawWaveform):
      integral = []
      for i in range(len(rawWaveform)):
         integral.append(np.sum(np.array(rawWaveform[i][self.wpretrigger-m2:self.wpretrigger+i1-m2])))
      integral = np.array(integral)
      return integral

  def peak_sum(self, rawWaveform):
      peak = []
      for i in range(len(rawWaveform)):
         peak.append(np.sum(np.array(rawWaveform[i][self.wpretrigger:self.wpretrigger+m1])))
      peak = np.array(peak)
      return peak

  def header_rawdata_compare(self, df):
      print('Comparing header and raw data...')
      df['WavePeak'].divide(df['PeakSum'])
      
      plt.hist(df['WavePeak'].divide(df['PeakSum']), bins=100, range=(0, 2), alpha=0.5)
      plt.xlabel('PeakSum Diff = WavePeak/PeakSum')
      plt.ylabel('Num of Entries')
      #plt.yscale('log')
      plt.savefig('.\plot\PeakSum_Diff_i1-'+str(i1)+'.png', dpi=150)
      #plt.show()
      plt.close()

      plt.hist(df['WaveInt'].divide(df['IntegratedSum']), bins=100, range=(0, 2), alpha=0.5)
      plt.xlabel('IntegratedSum Diff = WaveInt/IntgratedSum')
      plt.ylabel('Num of Entries')
      #plt.yscale('log')
      plt.savefig('.\plot\IntegratedSum_Diff_i1-'+str(i1)+'.png', dpi=150)
      #plt.show()
      plt.close()

      plt.hist(df['WaveBase'].divide(df['Info.mean']), bins=100, range=(0, 2), alpha=0.5)
      plt.xlabel('Baseline Diff = WaveBase/Info.mean')
      plt.ylabel('Num of Entries')
      #plt.yscale('log')
      plt.savefig('.\plot\Baseline_Diff_i1-'+str(i1)+'.png', dpi=150)
      plt.show()
      plt.close()
      '''
      plt.hist([df['WaveBase'], df['Info.mean']], bins=200, histtype='step', color=['navy', 'red'])
      plt.xlabel('Baseline')
      plt.ylabel('Num of Entries')
      plt.yscale('log')
      plt.savefig('.\plot\Baseline_i1-'+str(i1)+'.png', dpi=150)
      plt.show()
      plt.close()
      '''
      #print(df[['WaveBase', 'Baseline']].head(50))
      
  def integral_plot(self, df, channelID):
      print('Plotting histograms for recWaveform integral...')

      for id in channelID:
          df_ch = df.loc[df['ChannelID'] == id]['WaveInt']
          max_ch = df_ch.max()
          min_ch = df_ch.min()
          med_ch = df_ch.median()
          #print('Channel '+str(id)+' max integral: '+str(max_ch)+', min integral: '+str(min_ch))
          plt.hist(df_ch, bins=50, range=(min_ch, med_ch*2.0), alpha=0.5)
          plt.xlabel('Wave Integral of Channel '+str(id))
          plt.ylabel('Num of Entries')
          #plt.yscale('log')
          plt.savefig('.\plot\WInt_Ch_'+str(id)+'.png', dpi=150)
          plt.show()
          plt.close()
  def mean_waveform(self, waveform):
      print('Making mean waveform')

      mWaveform = np.mean(waveform, axis=0)
      binsslow  = np.array(range(570, 1200))

      plt.hist(range(0, self.wlength), bins=self.wlength, weights=mWaveform,  histtype='step', color='navy', linewidth=1, label='Mean Waveform, threshold > 50')
      plt.ylim(-0.1, 80)
      #plt.yscale('log')
      plt.xlabel('Time Tick [6.667 ns]')
      plt.ylabel('ADC Counts')
      
      popt, _ = curve_fit(exp_func, xdata=binsslow, ydata=mWaveform[570:1200], p0=[10, 0, 400])
      print(popt)
      x = np.linspace(550, 1500, 500)
      plt.plot(x, exp_func(x, *popt), 'r-', label=r"Exp-Fit, $\lambda$ = {:.2f}ns".format(round(popt[2]*6.6, 2)), linewidth=2) 
      
      plt.legend()      
      plt.savefig('.\plot\Meanwaveform.png', dpi=150)
      plt.show()
      plt.close()


      

  def waveform_plot(self, df, rawWaveform, recWaveform, channel):
      print('Plotting histograms for recWaveform from SiPM Channel '+str(channel)+' ...')
      
      indexLowInt = df[(df['WaveInt'] > 1400) & (df['WaveInt'] < 1600) & (df['ChannelID'] == channel)].index
      indexLowInt = indexLowInt.tolist()
      indexMedInt = df[(df['WaveInt'] > 1900) & (df['WaveInt'] < 2100) & (df['ChannelID'] == channel)].index
      indexMedInt = indexMedInt.tolist()
      indexHigInt = df[(df['WaveInt'] > 2500) & (df['ChannelID'] == channel)].index
      indexHigInt = indexHigInt.tolist()
      
      indexLowInt = random.sample(indexLowInt, 3)
      indexMedInt = random.sample(indexMedInt, 3)
      indexHigInt = random.sample(indexHigInt, 3)
      
      for i in indexLowInt:
          plt.hist(range(0, self.wlength), bins=self.wlength, weights=rawWaveform[i], histtype='step', color='navy', linewidth=0.5)
          plt.xlabel('Time Tick [6.667 ns]')
          plt.ylabel('ADC Counts')
          #plt.yscale('log')
          plt.savefig('.\plot\Ch_'+str(channel)+'-LowInt_Raw_Waveform_'+str(i)+'.png', dpi=150)
          plt.show()
          plt.close()
          
          plt.hist(range(0, self.wlength), bins=self.wlength, weights=recWaveform[i], histtype='step', color='red', linewidth=0.5)
          plt.xlabel('Time Tick [6.667 ns]')
          plt.ylabel('ADC Counts')
          #plt.yscale('log')
          plt.savefig('.\plot\Ch_'+str(channel)+'-LowInt_Rec_Waveform_'+str(i)+'.png', dpi=150)
          plt.show()
          plt.close()
          
      for i in indexMedInt:
          plt.hist(range(0, self.wlength), bins=self.wlength, weights=rawWaveform[i], histtype='step', color='navy', linewidth=0.5)
          plt.xlabel('Time Tick [6.667 ns]')
          plt.ylabel('ADC Counts')
          #plt.ylim(1450, 1700)
          #plt.yscale('log')
          plt.savefig('.\plot\Ch_'+str(channel)+'-MedInt_Raw_Waveform_'+str(i)+'.png', dpi=150)
          plt.show()
          plt.close()
          
          plt.hist(range(0, self.wlength), bins=self.wlength, weights=recWaveform[i], histtype='step', color='red', linewidth=0.5)
          plt.xlabel('Time Tick [6.667 ns]')
          plt.ylabel('ADC Counts')
          #plt.yscale('log')
          plt.savefig('.\plot\Ch_'+str(channel)+'-MedInt_Rec_Waveform_'+str(i)+'.png', dpi=150)
          plt.show()
          plt.close()
          
      for i in indexHigInt:
          plt.hist(range(0, self.wlength), bins=self.wlength, weights=rawWaveform[i], histtype='step', color='navy', linewidth=0.5)
          plt.xlabel('Time Tick [6.667 ns]')
          plt.ylabel('ADC Counts')
          #plt.ylim(1450, 1700)
          #plt.yscale('log')
          plt.savefig('.\plot\Ch_'+str(channel)+'-HighInt_Raw_Waveform_'+str(i)+'.png', dpi=150)
          plt.show()
          plt.close()
          
          plt.hist(range(0, self.wlength), bins=self.wlength, weights=recWaveform[i], histtype='step', color='red', linewidth=0.5)
          plt.xlabel('Time Tick [6.667 ns]')
          plt.ylabel('ADC Counts')
          #plt.yscale('log')
          plt.savefig('.\plot\Ch_'+str(channel)+'-HighInt_Rec_Waveform_'+str(i)+'.png', dpi=150)
          plt.show()
          plt.close()
          
  # def photon_analysis(header, ch1, ch2, ch4, ch5, ch6, ch7, ch8):
  #   import_file(header, ch1, ch2, ch4, ch5, ch6, ch7, ch8)
  #   for i in range(len(df['Waveform'])):

  def trig_per_channel(self, df):
      category = Counter(df['ChannelID'])
      return category.keys(), category.values()
      # Option 2:
      # trignum = []
      # for i in range(1, 8):
      #     trignum.append(df['ChannelID'].count(i))
                     
      # Option 3:
      # trignum = []
      # for i in range(1, 8):
      #   count = 0
      #   if df['ChannelID'] == i:
      #     count += 1
      #   trignum.append(count)
      # return trignum

  def trig_rate(self, df, channelID):
      category = Counter(df['ChannelID'])
      
      for id in channelID:
          if(len(df[df['ChannelID']==id])>0):
              time_cycle = np.max(df[ (df['ChannelID'] == id) ]['timestamp_S']) - np.min(df[ (df['ChannelID'] == id) ]['timestamp_S'])
              rate       = category[id]/time_cycle
              print('Channel '+str(id)+' trigger rate: '+str(rate))


  def noise_compare(self, rawWaveform, event): #Event column in header file, identifies which recWaveform to analyze
      noise_std = np.std(rawWaveform[event][:self.pretrigger-10])
      peak_height = np.max(rawWaveform[event][self.pretrigger-10:self.pretrigger+50])
      print('Background Standard Deviation: '+str(noise_std)+' Peak Height: '+str(peak_height))

  def intsum_plot(self, df, channelID, lwleng):
      print('Plotting histograms for integrated sum...')
  
      for id in channelID:
          if(len(df[df['ChannelID']==id])>0):
              print('Channel: ', id)
              df_intsum   = df.loc[df['ChannelID'] == id]['IntegratedSum']              
              df_baseline = df.loc[df['ChannelID'] == id]['Info.mean']
              df_intsum   = df_intsum - df_baseline*250

              if(id == 2):
                  path = r'.\Int_Sum_Channel_'+str(id)+'.log'
                  with open(path, 'a') as f:
                      df_string = df_intsum.to_string(header=False, index=False)
                      f.write(df_string)

              min_intsum  = df_intsum.min()
              max_intsum  = df_intsum.max()
              med_intsum  = df_intsum.median()

              df_intEn   = df.loc[df['ChannelID'] == id]['Info.intEnergy']

              plt.hist([df_intsum], bins=100, range=(0, med_intsum*4.0), histtype='step', color=['navy'], alpha=0.5)
              plt.xlabel('IntegratedSum (basline subtraction) of Channel '+str(id))
              plt.ylabel('Num of Entries')
              #plt.yscale('log')
              plt.savefig('.\plot\IntegratedSum_baseline_subtraction_Ch_'+str(id)+'_wlength_'+lwleng+'.png', dpi=150)
              plt.show()
              plt.close()
  
def dark_noise(df, channelID, llevel, lwleng):
   print('Plotting histograms for dark noise...')

   for id in channelID:
       if(len(df[df['ChannelID']==id])>0):
           print('Channel: ', id)
           df_intsum   = df.loc[df['ChannelID'] == id]['IntegratedSum']    
           df_peaksum  = df.loc[df['ChannelID'] == id]['PeakSum']
           df_baseline = df.loc[df['ChannelID'] == id]['Prerise']
           
           min_intsum  = df_intsum.min()
           med_intsum  = df_intsum.median()
           plt.hist([df_intsum], bins=500, histtype='step', color=['red'], alpha=0.5)
           plt.xlabel(lwleng+' IntSum of Channel '+str(id)+' LLevel '+llevel[1:])
           plt.ylabel('Num of Entries')
           plt.yscale('log')
           plt.savefig('.\plot\IntSum_Ch_'+str(id)+'_'+lwleng+'_'+llevel[1:]+'.png', dpi=150)
           plt.show()
           plt.close()
           
           min_peaksum = df_peaksum.min()           
           med_peaksum = df_peaksum.median()
           plt.hist([df_peaksum], bins=500, histtype='step', color=['green'], alpha=0.5)
           plt.xlabel(lwleng+' PeakSum of Channel '+str(id)+' LLevel '+llevel[1:])
           plt.ylabel('Num of Entries')
           plt.yscale('log')
           plt.savefig('.\plot\PeakSum_Ch_'+str(id)+'_'+lwleng+'_'+llevel[1:]+'.png', dpi=150)
           plt.show()
           plt.close()

           df_intsum   = df_intsum - df_baseline
           med_intsum  = df_intsum.median()
           plt.hist([df_intsum], bins=500, histtype='step', color=['navy'], alpha=0.5)
           plt.xlabel(lwleng+' IntSum (basline subtraction) of Channel '+str(id)+' LLevel '+llevel[1:])
           plt.ylabel('Num of Entries')
           plt.yscale('log')
           plt.savefig('.\plot\IntSum_baseline_subtraction_Ch_'+str(id)+'_'+lwleng+'_'+llevel[1:]  +'.png', dpi=150)
           plt.show()
           plt.close()

def exp_func(x, a, b, c):
    return a * ((1-b)*np.exp(-x/c) + b)


########
# main #
########

def main():
    parser = argparse.ArgumentParser(description='Waveforem analysis software for the LArS experiment')
    
    # Define the arguments
    parser.add_argument('-p', '--path',       default=r'C:\Muve\dune\larscattering\data\lifetime\waveform', help='where to load the files')
    parser.add_argument('-l', '--llevel',     default=r'\9.5tin',                               help='liquid level: xxtin')
    parser.add_argument('-w', '--wavelength', default='closed',                                 help='photon wavelength: xxxxA')
    parser.add_argument('-r', '--runnumber',  default='2',                                     help="ssp run number")
    parser.add_argument('-d', '--datatime',   default='2023-08-09_11-16-08',                   help="YYYY-MM-DD_HH-MM-SS")
    parser.add_argument('-t', '--pretrigger', type=int,        default=500,                    help='length of pretrigger window')
    parser.add_argument('-f', '--wflength',   type=int,        default=2000,                   help='length of recWaveform window')
    
    # Parse the arguments
    args = parser.parse_args()
	
    fpath  = args.path
    llevel = args.llevel
    lwleng = args.wavelength
    runnum = args.runnumber
    dtime  = args.datatime
    lpretr = args.pretrigger
    lwflen = args.wflength
    
    header = fpath+llevel+'_'+lwleng+'-'+runnum+'_'+dtime+'.csv'
    ch1    = fpath+llevel+'_'+lwleng+'_Ch1-'+runnum+'_'+dtime+'.dat'
    ch2    = fpath+llevel+'_'+lwleng+'_Ch2-'+runnum+'_'+dtime+'.dat'
    ch4    = fpath+llevel+'_'+lwleng+'_Ch4-'+runnum+'_'+dtime+'.dat'
    ch5    = fpath+llevel+'_'+lwleng+'_Ch5-'+runnum+'_'+dtime+'.dat'
    ch6    = fpath+llevel+'_'+lwleng+'_Ch6-'+runnum+'_'+dtime+'.dat'
    ch7    = fpath+llevel+'_'+lwleng+'_Ch7-'+runnum+'_'+dtime+'.dat'
    ch8    = fpath+llevel+'_'+lwleng+'_Ch8-'+runnum+'_'+dtime+'.dat'
    
    #data_files = [ch1, ch2, ch4, ch5, ch6, ch8]    
    data_files = [ch2]
    channelID = [2]

    ana = Analysis(lwleng, lwflen, lpretr, 24)
    print('Photon wavelength: '+lwleng+' recWaveform length: '+str(lwflen)+' pretrigger length: '+str(lpretr))
    if len(data_files) > 0:
        df, rawWaveform, recWaveform  = ana.import_file(header, data_files)
    else:
        df = ana.import_file(header, data_files)
        
    ana.mean_waveform(rawWaveform)    
    #ana.header_rawdata_compare(df)    
    #ana.integral_plot(df, channelID)
    #for id in channelID:
    #    ana.waveform_plot(df, rawWaveform, recWaveform, id)    
    #ana.trig_rate(df, channelID)
    #ana.intsum_plot(df, channelID, lwleng)

    #dark_noise(df, channelID, llevel, lwleng)
    
if __name__ == '__main__':   
    main()    
    
