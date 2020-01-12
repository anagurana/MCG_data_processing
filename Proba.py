#!/usr/bin/env python3
from scipy import *
from scipy import signal
from scipy.signal import lfilter, freqz, butter, filtfilt
from psd import *
import matplotlib.pyplot as plt
from biosppy.signals import ecg
import numpy as np

# Sample frequency
Fs = 1000 # Hz
def notchFitler(data, Fs, frequency, Q):
    nyquistFrequency = Fs/2.
    normalizedCutoff = frequency/nyquistFrequency
    b,a = signal.iirnotch(w0=normalizedCutoff, Q=Q)
    xfiltered = signal.filtfilt(b,a,data)
    return xfiltered
def lowFilter(data, Fs, highFrequency):
    nyquistFrequency = Fs / 2.
    normalizedCutoff = highFrequency / nyquistFrequency
    b,a = signal.butter(5, normalizedCutoff, btype='low')
    return filtfilt(b, a, data)
def highFilter(data, Fs, lowFrequency ):
    nyquistFrequency = Fs / 2.
    normalizedCutoff = lowFrequency / nyquistFrequency
    b, a = signal.butter(5, normalizedCutoff, btype='high')
    return filtfilt(b, a, data)
def bandpassFilter(data, Fs, lowf, highf):
    nyquistFrequency = Fs / 2.
    normalizedCutoffH = highf / nyquistFrequency
    normalizedCutoffL = lowf / nyquistFrequency
    b,a = signal.butter(5, [normalizedCutoffL, normalizedCutoffH], btype='band')
    return lfilter(b, a, data)
def allWithOne (signal, lowf, highf, Fs, Q, notch1, notch2):
    y1 = highFilter(signal, Fs, lowf)
    y1 = lowFilter(y1, Fs, highf)
    y1 = notchFitler(y1, Fs, notch1, Q)
    y1 = notchFitler(y1, Fs, notch2, Q)
    return y1
def hpException (signal, highf, Fs, Q, notch1, notch2):
    y1 = lowFilter(signal, Fs, highf)
    y1 = notchFitler(y1, Fs, notch1, Q)
    y1 = notchFitler(y1, Fs, notch2, Q)
    return y1
def peaksAndAveraged (signal, visibility):
    out = ecg.ecg(signal, sampling_rate= Fs, show = visibility)
    rpeaks = out['rpeaks']
    templates = out['templates']
    average_final = np.average(templates, axis=0)
    return rpeaks, average_final, templates
def powerSpectral (signal):
    freqs, psd1 = powerSpectralDensity(signal, Fs)
    #Plot spectrum
    plt.loglog(freqs, psd1)
    plt.xlabel("Czestotliwość (Hz)")
    plt.ylabel("Amplituda (pT)")
    plt.grid()
    plt.show()
def plotAvereged (templates, average_final):
    ts_tmpl = np.linspace(0, 0.6, templates.shape[1], endpoint=False)
    plt.plot(ts_tmpl, average_final)
    plt.xlabel("Czas (s)")
    plt.ylabel("Amplituda (pT)")
    plt.grid()
    plt.show()


#File loading
filename = "Tom II MCG.tsv"
#filename = "janmasny_MKG3.txt"
#filename = "janmasny_MKG2.txt"
#filename = "szumy (1).txt"

data = loadtxt(filename)
y1 = data[:,1]
y2 = data[:,3]*0.5

# Clip out good data

#Szerszy zakres szumy
#y1 = y1[30000:80000]

#for presentation
#y1 = y1[91000:99000]
#y2= y2[91000:99000]

#y1 = y1[130000:170000]
#y1 = y1[41000:50000]

#czyba dobrze na 2 kanalach
#y1 = y1[64000:73500]
#y2= y2[64000:73500]

#wiekszy zakres
y1 = y1[5500:80000]
y2 = y2[5500:80000]

times = arange(len(y1))/Fs

# HP filters
'''y1 = highFilter (y1, Fs, lowFrequency=1)
y2 = highFilter (y2, Fs, lowFrequency=0.3)'''
y1 = allWithOne (y1, lowf = 1, highf=100, Fs=Fs, Q=50, notch1=50, notch2=100)
y2 = allWithOne (y2, lowf = 0.3, highf=100, Fs=Fs, Q=50, notch1=50, notch2=100)
#Plot timeseries for avereged signal
ave2sensors=(y1+y2)/2                                           #Averaging signals
#powerSpectral (ave2sensors)
rpeaks, average_final, templates = peaksAndAveraged (ave2sensors, False)
#Peaks detection
plt.scatter(rpeaks/1000, ave2sensors[rpeaks], c='red')
plt.plot(times, ave2sensors)
#Graphs labels
plt.xlabel("Czas (s)")
plt.ylabel("Amplituda (pT)")
plt.grid()
plt.show()
#pl1 = plotAvereged (templates, average_final)                         #Averaged signal

#Plot timeseries for both signals
#powerSpectral (y1)
#powerSpectral (y2)
rpeaks1, average_final1, templates1 = peaksAndAveraged (y1, False)
rpeaks2, average_final2, templates2 = peaksAndAveraged (y2, False)

fig, axs = plt.subplots(2)
fig.suptitle('Sygnały z dwóch czujników')
axs[0].plot(times, y1, 'tab:orange')
axs[0].set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
axs[0].scatter(rpeaks1/1000, y1[rpeaks1], c='red')
axs[0].grid()
axs[1].set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
axs[1].plot(times, y2, 'tab:red')
axs[1].scatter(rpeaks2/1000, y2[rpeaks2], c='red')
axs[1].grid()
plt.show()

#Averaged signal
#pl2 = plotAvereged (templates1, average_final1)
#pl3 = plotAvereged (templates2, average_final2)

fig, axs = plt.subplots(3)
ts_tmpl = np.linspace(0, 0.6, templates.shape[1], endpoint=False)
axs[0].plot(ts_tmpl, average_final1)
axs[0].grid()
#axs[0].set_title ('Pierwszy czyjnik')
axs[1].plot(ts_tmpl, average_final2)
axs[1].grid()
#axs[1].set_title ('Drugi czyjnik')
axs[2].plot(ts_tmpl, average_final)
axs[2].grid()
#axs[2].set_title ('Uśredniony z obu czujników')
for ax in axs.flat:
    ax.set(xlabel='Czas (ms)', ylabel='Amplituda (pT)')
plt.show()