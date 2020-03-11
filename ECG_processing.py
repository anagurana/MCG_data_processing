from scipy import *
from scipy import signal
from scipy.signal import lfilter, freqz, butter, filtfilt
from psd import *
import matplotlib.pyplot as plt
from biosppy.signals import ecg
import numpy as np
import matplotlib

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
def peaksAndAveraged (signal, visibility):
    forTemplates = ecg.ecg(signal, sampling_rate= Fs, show = visibility)
    forPeaks = ecg.ecg(signal, sampling_rate=Fs, show=visibility)
    rpeaks = forPeaks['rpeaks']
    templates = forTemplates['templates']
    average_final = np.average(templates, axis=0)
    return rpeaks, average_final, templates
def move_figure(f, x, y):
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        f.canvas.manager.window.move(x, y)

# File loading
filename = "Tom II MCG.tsv"

data = loadtxt(filename)
data1Sensor = data[:,1]*2.4
data2Sensor = data[:,3]*0.9

# data1Sensor = data[:,1]*2.2
# data2Sensor = data[:,3]*0.8

# Clip out good data

y1 = data1Sensor[5500:80000]
y2 = data2Sensor[5500:80000]

# For 100 heart beats
# y1=data1Sensor[1000:97000]
# y2=data2Sensor[1000:97000]

# For 50 heart beats
# y1=data1Sensor[1000:47000]
# y2=data2Sensor[1000:47000]

# For 25 heart beats
# y1=data1Sensor[1000:23000]
# y2=data2Sensor[1000:23000]

# For 12 heart beats
# y1=data1Sensor[1000:11200]
# y2=data2Sensor[1000:11200]

# For 8 heart beats (Presentation)
# y1=data1Sensor[11000:21000]
# y2=data2Sensor[11000:21000]

# For 6 heart beats
y1=data1Sensor[1000:6500]
y2=data2Sensor[1000:6500]


# Filters
Fs = 1000 # Hz

yFiltered1= highFilter (y1, Fs, lowFrequency=2)
yFiltered2 = highFilter (y2, Fs, lowFrequency=1)

yFiltered1 = notchFitler(yFiltered1, Fs, 50, 15)
yFiltered1 = notchFitler(yFiltered1, Fs, 35, 10)
yFiltered1 = notchFitler(yFiltered1, Fs, 45, 22.5)
yFiltered1 = notchFitler(yFiltered1, Fs, 100, 50)


yFiltered2 = notchFitler(yFiltered2, Fs, 50, 15)
yFiltered2 = notchFitler(yFiltered2, Fs, 35, 10)
yFiltered2 = notchFitler(yFiltered2, Fs, 45, 22.5)
yFiltered2 = notchFitler(yFiltered2, Fs, 100, 50)

yFiltered1 = lowFilter(yFiltered1, Fs, 30)
yFiltered2 = lowFilter(yFiltered2, Fs, 30)

# Finding peaks

rpeaks1, average_final1, templates1 = peaksAndAveraged (yFiltered1, False)
rpeaks2, average_final2, templates2 = peaksAndAveraged (yFiltered2, False)
ts_tmpl = np.linspace(0, 0.7, templates1.shape[1], endpoint=False)

print("Number of cycles = ", templates1.shape[0])

###     Drawing Plots   ###

# Power Spectral Density
fig, axs = plt.subplots(1,2, figsize = (19,7))
move_figure(fig, 0, 0)
fig.suptitle('Widmo mocy')
freqs, psd1 = powerSpectralDensity(yFiltered1, Fs)
axs[0].semilogy(freqs, psd1, 'tab:orange')
freqs, psd2 = powerSpectralDensity(yFiltered2, Fs)
axs[1].semilogy(freqs, psd2)
for ax in axs.flat:
    ax.set(xlabel='Częstotliwość (pT)', ylabel='Amplituda (pT)')
    ax.set_xscale('log')
    ax.grid()
plt.show()

# Signals from 2 sensors
times = arange(len(yFiltered1))/Fs
fig, axs = plt.subplots(2, figsize = (19,7))
move_figure(fig, 0, 0)
fig.suptitle('Sygnały z 2 czujników')
axs[0].plot(times, yFiltered1, 'tab:orange')
# axs[0].scatter(rpeaks1/1000, yFiltered1[rpeaks1])
axs[1].plot(times, yFiltered2)
# axs[1].scatter(rpeaks2/1000, yFiltered2[rpeaks2], c='orange')
for ax in axs.flat:
    ax.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
    ax.grid()
plt.show()

# Overlapping signals
fig, axs = plt.subplots(1,2, figsize = (19,7))
move_figure(fig, 0, 0)
fig.suptitle('Nałożone sygnały')
for beat in range(0,templates1.shape[0]):
    axs[0].plot(ts_tmpl, templates1[beat,:], 'tab:orange')
for beat in range(0, templates2.shape[0]):
    axs[1].plot(ts_tmpl, templates2[beat,:], '#1f77b4')
for ax in axs.flat:
    ax.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
    ax.grid()
plt.show()

# Averaged signals
fig, axs = plt.subplots(1, 2, figsize = (19,7))
move_figure(fig, 0, 0)
fig.suptitle('Uśredniony sygnał')
axs[0].plot(ts_tmpl, average_final1, 'tab:orange')
axs[1].plot(ts_tmpl, average_final2)
for ax in axs.flat:
    ax.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
    ax.grid()
plt.show()