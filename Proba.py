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
def notchFitler(data, Fs, frequency = 16.5, Q = 10):
    nyquistFrequency = Fs/2.
    normalizedCutoff = frequency/nyquistFrequency
    b,a = signal.iirnotch(w0=normalizedCutoff, Q=Q)
    xfiltered = signal.filtfilt(b,a,data)
    return xfiltered
def lowFilter(data, Fs, frequency = 16.5):
    nyquistFrequency = Fs / 2.
    normalizedCutoff = frequency / nyquistFrequency
    b,a = signal.butter(5, normalizedCutoff, btype='low')
    return filtfilt(b, a, data)
def highFilter(data, Fs, frequency ):
    nyquistFrequency = Fs / 2.
    normalizedCutoff = frequency / nyquistFrequency
    b, a = signal.butter(5, normalizedCutoff, btype='high')
    return filtfilt(b, a, data)
def bandpassFilter(data, Fs, lf, hf):
    nyquistFrequency = Fs / 2.
    normalizedCutoffH = hf / nyquistFrequency
    normalizedCutoffL = lf / nyquistFrequency
    b,a = signal.butter(5, [normalizedCutoffL, normalizedCutoffH], btype='band')
    return lfilter(b, a, data)
def allWithOne (signal, lf, hf, Fs, Q, notch1, notch2):
    y1 = highFilter(signal, Fs, lf)
    y1 = lowFilter(y1, Fs, hf)
    y1 = notchFitler(y1, Fs, notch1, Q)
    y1 = notchFitler(y1, Fs, notch2, Q)
    return y1
def hpException (signal, hf, Fs, Q, notch1, notch2):
    y1 = lowFilter(signal, Fs, hf)
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
    #zmienic na skumulowany jednokrotnie
    freqs, psd1 = powerSpectralDensity(signal, Fs)
    #Plot spectrum
    plt.loglog(freqs, psd1)
    plt.xlabel("Czestotliwość (Hz)")
    plt.ylabel("Amplituda (pT)")
    plt.grid()
    plt.show()
def plotAvereged (templates, average_final):
    ts_tmpl = np.linspace(-0.2, 0.4, templates.shape[1], endpoint=False)
    plt.plot(ts_tmpl, average_final)
    plt.xlabel("Time (s)")
    plt.ylabel("Signal (pT)")
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

#Szerdy zakres szumy
#y1 = y1[30000:80000]

#for presentation
#y1 = y1[91000:99000]
#y2= y2[91000:99000]

#y1 = y1[130000:170000]
#y1 = y1[41000:50000]

#czyba dobrze na 2 kanalach
y1 = y1[64000:73500]
y2= y2[64000:73500]
times = arange(len(y1))/Fs

# HP filters
y1 = highFilter (y1, Fs, 1)
y2 = highFilter (y2, Fs, 0.3)

'''#Plot timeseries for avereged signal
ave2sensors=(y1+y2)/2                                           #Averaging signals
powerSpectral (ave2sensors)
ave2sensors = hpException (ave2sensors, 80, Fs, 50, 50, 100)
rpeaks, average_final, templates = peaksAndAveraged (ave2sensors, True)
#Peaks detection
plt.scatter(rpeaks/1000, ave2sensors[rpeaks], c='red')
plt.plot(times, ave2sensors)
#Graphs labels
plt.xlabel("Czas (s)")
plt.ylabel("Amplituda (pT)")
plt.grid()
plt.show()
plotAvereged (templates, average_final)                         #Averaged signal'''


#Plot timeseries for both signals
y1 = hpException (y1, 80, Fs, 50, 50, 100)
y2 = hpException (y2, 80, Fs, 50, 50, 100)
#powerSpectral (y1)
#powerSpectral (y2)
rpeaks1, average_final1, templates1 = peaksAndAveraged (y1, False)
rpeaks2, average_final2, templates2 = peaksAndAveraged (y2, False)
#Peaks detection
plt.scatter(rpeaks1/1000, y1[rpeaks1]+60, c='red')
plt.scatter(rpeaks2/1000, y2[rpeaks2], c='red')
plt.plot(times, y1+60)
plt.plot(times, y2)
#Graphs labels
plt.xlabel("Czas (s)")
plt.ylabel("Amplituda (pT)")
plt.grid()
plt.show()
plotAvereged (templates1, average_final1)                                  #Averaged signal
plotAvereged (templates2, average_final2)

fig, axs = plt.subplots(2)
fig.suptitle('Sygnały z dwóch czujników')
axs[0].plot(times, y1, 'tab:orange')
axs[1].plot(times, y1, 'tab:red')
axs[0].set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
axs[1].set(xlabel='Czas (s)', ylabel='Amplituda (pT)')


