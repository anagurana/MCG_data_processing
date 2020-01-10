#!/usr/bin/env python3
from scipy import *
from scipy import signal
from psd import * 
import matplotlib.pyplot as plt

filename = "Sylwia Heart.tsv"
data = loadtxt(filename)

x1 = data[:,0]
y1 = data[:,1]
x2 = data[:,2]
y2 = data[:,3]

# Sample frequency
Fs = 10000/12/4 # Hz

def notchFitler(x, Fs, frequency = 16.5, Q = 10):
    nyquistFrequency = Fs/2.
    normalizedCutoff = frequency/nyquistFrequency
    b,a = signal.iirnotch(w0=normalizedCutoff, Q=Q)
    xfiltered = signal.filtfilt(b,a,x)
    return xfiltered

y1 = notchFitler(y1, Fs, frequency = 16.5, Q = 20)
y1 = notchFitler(y1, Fs, frequency = 50, Q = 100)
#y = notchFitler(y, Fs, frequency = 10, Q = 1)

y2 = notchFitler(y2, Fs, frequency = 16.5, Q = 20)
y2 = notchFitler(y2, Fs, frequency = 50, Q = 100)

freqs, psd1 = powerSpectralDensity(y1, Fs)
freqs, psd2 = powerSpectralDensity(y2, Fs)

#Plot spectrum
plt.loglog(freqs, psd2)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Signal (pT)")
plt.show()

# Clip out good data
y1 = y1[7622:8533]
y2 = y2[7622:8533]
times = arange(len(y1))/Fs

#Plot timeseries
plt.plot(times, y1)
plt.plot(times, y2+25)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Signal (pT)")
plt.show()
