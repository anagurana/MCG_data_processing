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

filename = "Mapowanie+potencjaly_wylowane/Kompensacja.txt"
data = loadtxt(filename)
y1 = data[:,1]

file = 'Mapowanie+potencjaly_wylowane/Kompensacja_czujnika.txt'
data = loadtxt(file)
x1=data [:,1]

###############################################################

y2=y1[10000:30000]
y2 = highFilter(y2, 1000, 1)
y2=(absolute(y2))
print(mean(y2))
print (max(y2))
y3=y1[140000:170000]
y3 = highFilter(y3, 1000, 1)
y3=(absolute(y3))
print(mean(y3))
print (max(y3))
y4=y1[246000:276000]
y4 = highFilter(y4, 1000, 1)
y4=(absolute(y4))
print(mean(y4))
print (max(y4))

x1=x1[10000:30000]
x1 = highFilter(x1, 1000, 1)
x1=(absolute(x1))
print(mean(x1))
print (max(x1))


times = arange(len(x1))/Fs
powerSpectral (x1)
plt.plot(times, x1)
plt.grid()
plt.show()

##################################################################

'''#Klatka otwarta
y2=y1[14000:19000]
#Klatka zamknięta
y3=y1[144000:149000]
#Kompensacja aktywna
y4=y1[248500:253500]
#Kompensacja czujnika
x=x1[35000:40000]

times = arange(len(y2))/Fs
fig, (axs1, axs2) = plt.subplots(1,2)
axs1.plot(times, y2)
axs1.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
axs1.grid()
powerSpectral (y1[10000:30000])

times = arange(len(y3))/Fs
fig, (axs1, axs2) = plt.subplots(1,2)
axs1.plot(times, y3)
axs1.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
axs1.grid()
powerSpectral (y1[140000:170000])

times = arange(len(y4))/Fs
fig, (axs1, axs2) = plt.subplots(1,2)
axs1.plot(times, y4)
axs1.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
axs1.grid()
powerSpectral (y1[246000:276000])

times = arange(len(x))/Fs
fig, (axs1, axs2) = plt.subplots(1,2)
axs1.plot(times, x)
axs1.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
axs1.grid()
powerSpectral (x1[10000:30000])'''