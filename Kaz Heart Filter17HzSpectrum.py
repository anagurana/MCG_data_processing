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

filename = "Tom II MCG.tsv"
#filename = "janmasny_MKG3.txt"
#filename = "janmasny_MKG2.txt"
#filename = "szumy (1).txt"

data = loadtxt(filename)
y1 = data[:,1]
y2 = data[:,3]*0.5

# Clip out good data
#y1 = y1[41000:50000]

#Szerdy zakres szumy
#y1 = y1[30000:80000]

#for presentation
y1 = y1[91000:99000]
y2= y2[91000:99000]

#y1 = y1[130000:170000]

times = arange(len(y1))/Fs

# HP filters
y1 = highFilter (y1, Fs, 1)
y2 = highFilter (y2, Fs, 0.3)

#when we want to do all in the 2 signal
#y1 = highFilter (y2, Fs, 1)

#averaging signals
#y1=(y1+y2)/2

#LP filter + notch (selecting frequency)
y1 = lowFilter(y1, Fs, frequency = 30)
y1 = notchFitler(y1, Fs, frequency = 50, Q = 50)
y1 = notchFitler(y1, Fs, frequency = 100, Q = 50)
#y1 = notchFitler(y1, Fs, frequency = 150, Q = 150)

out = ecg.ecg(signal=y1, sampling_rate=Fs, show = True)
rpeaks = out['rpeaks']
templates = out['templates']
average_final = np.average(templates, axis=0)

#zmienic na skumulowany jednokrotnie
freqs, psd1 = powerSpectralDensity(y1, Fs)


#Plot spectrum
plt.loglog(freqs, psd1)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Signal (pT)")
plt.grid()
plt.show()

#Plot timeseries for both signals
#plt.plot(times, y1+60)
#plt.plot(times, y2)

#Plot timeseries for one signal
plt.plot(times, y1)

#peaks detection
plt.scatter(rpeaks/1000, y1[rpeaks], c='red' )

plt.xlabel("Time (s)")
plt.ylabel("Signal (pT)")
plt.grid()
plt.show()

ts_tmpl = np.linspace(-0.2, 0.4, templates.shape[1], endpoint=False)

plt.plot(ts_tmpl, average_final)
plt.xlabel("Time (s)")
plt.ylabel("Signal (pT)")
plt.show()
#savetxt('data.txt', y1, '%10.5f


