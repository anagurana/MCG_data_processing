from scipy import *
from scipy import signal
from scipy.signal import lfilter, freqz, butter, filtfilt
from psd import *
import matplotlib.pyplot as plt
from biosppy.signals import ecg
import numpy as np
import matplotlib


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
def peaksAndAveraged (signal, visibility):
    forTemplates = ecg.ecg(signal, sampling_rate= Fs, show = visibility)
    filtered = signal
    # filtered = highFilter(signal, Fs, 5)
    # filtered = lowFilter(filtered, Fs, 15)
    forPeaks = ecg.ecg(filtered, sampling_rate=Fs, show=visibility)
    # rpeaks = ecg.hamilton_segmenter(filtered, Fs)
    rpeaks = forPeaks['rpeaks']
    templates = forTemplates['templates']
    average_final = np.average(templates, axis=0)
    return rpeaks, average_final, templates
def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)

#File loading
filename = "Tom II MCG.tsv"
#filename = "janmasny_MKG3.txt"

data = loadtxt(filename)
data1 = data[:,1]*2.4
data2 = data[:,3]*0.9

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
# yw1 = data1[5500:80000]
# yw2 = data2[5500:80000]

#Dla 100 cykli
yw1=data1[1000:97000]
yw2=data2[1000:97000]

#Dla 50 cykli
# yw1=data1[1000:47000]
# yw2=data2[1000:47000]

#Dla 25 cykli
# yw1=data1[1000:23000]
# yw2=data2[1000:23000]

#Dla 12 cykli
# yw1=data1[1000:11200]
# yw2=data2[1000:11200]

#Dla 6 cykli
# yw1=data1[1000:6500]
# yw2=data2[1000:6500]

#Filters
yw1= highFilter (yw1, Fs, lowFrequency=2)
yw2 = highFilter (yw2, Fs, lowFrequency=1)

yw1 = notchFitler(yw1, Fs, 50, 2.5)
yw1 = notchFitler(yw1, Fs, 23, 23)
yw1 = notchFitler(yw1, Fs, 100, 50)

yw2 = notchFitler(yw2, Fs, 50, 2.5)
yw2 = notchFitler(yw2, Fs, 60, 20)
yw2 = notchFitler(yw2, Fs, 100, 50)

yw1 = lowFilter(yw1, Fs, 30)
yw2 = lowFilter(yw2, Fs, 30)

# y1=yw1[5500:15500]
# y2=yw2[5500:15500]

#Prezentacja
# y1=yw1[5500:13000]
# y2=yw2[5500:13000]

y1=yw1
y2=yw2

times = arange(len(y1))/Fs

'''#Plot timeseries for avereged signal
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
#pl1 = plotAvereged (templates, average_final)                         #Averaged signal'''

#Plot timeseries for both signals

rpeaks1, average_final1, templates1 = peaksAndAveraged (y1, False)
rpeaks2, average_final2, templates2 = peaksAndAveraged (y2, False)
ts_tmpl = np.linspace(0, 0.6, templates1.shape[1], endpoint=False)

#Ploty


fig, axs = plt.subplots(1,2, figsize = (19,7))
move_figure(fig, 0, 0)
#fig.suptitle('Power Spectral Density')
freqs, psd1 = powerSpectralDensity(yw1, Fs)
axs[0].semilogy(freqs, psd1, 'tab:orange')
freqs, psd2 = powerSpectralDensity(yw2, Fs)
axs[1].semilogy(freqs, psd2)
for ax in axs.flat:
    ax.set(xlabel='Częstotliwość (pT)', ylabel='Amplituda (pT)')
    ax.set_xscale('log')
    ax.grid()
plt.show()

fig, axs = plt.subplots(2, figsize = (19,7))
move_figure(fig, 0, 0)
#fig.suptitle('Signals from 2 sensors')
axs[0].plot(times, y1, 'tab:orange')
axs[0].scatter(rpeaks1/1000, y1[rpeaks1])
axs[1].plot(times, y2)
axs[1].scatter(rpeaks2/1000, y2[rpeaks2], c='orange')
for ax in axs.flat:
    ax.set(xlabel='Czas (s)', ylabel='Amplituda (pT)')
    ax.grid()
plt.show()


fig, axs = plt.subplots(1,2, figsize = (19,7))
move_figure(fig, 0, 0)
#fig.suptitle('Nałożone sygnały')
for beat in range(0,templates1.shape[0]):
    axs[0].plot(ts_tmpl, templates1[beat,:], 'tab:orange')
for beat in range(0, templates2.shape[0]):
    axs[1].plot(ts_tmpl, templates2[beat,:], '#1f77b4')
for ax in axs.flat:
    ax.set(xlabel='Czas (ms)', ylabel='Amplituda (pT)')
    ax.grid()
plt.show()


fig, axs = plt.subplots(1, 2, figsize = (19,7))
move_figure(fig, 0, 0)
#fig.suptitle('Averaged signals')
axs[0].plot(ts_tmpl, average_final1, 'tab:orange')
axs[1].plot(ts_tmpl, average_final2)
for ax in axs.flat:
    ax.set(xlabel='Czas (ms)', ylabel='Amplituda (pT)')
    ax.grid()
plt.show()