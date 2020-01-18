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
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja1.txt"
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja2.txt"
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja3.txt"
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja4.txt" # na minusie
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja5.txt"
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja6.txt"
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja7.txt"
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja8.txt" #na minusie
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja9.txt" #na minusie
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja10.txt" #na minusie
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja11.txt" # na minusie
# filename = "Mapowanie+potencjaly_wylowane/mkg2_anastasiya_pozycja12.txt" # na minusie


#Wszystko robie dla 30 usrednien
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja1.txt"       #  90U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja2.txt"       # 2 części: 1 - 88U, 2 - 74U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja3.txt"       # 3 części: 1 - 85U, 2 - 72U, 3 - 33U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja4.txt"       # 21U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja5.txt"       # 44U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja6.txt"       # 44U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja7.txt"       # 67U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja8.txt"       # 8 oraz 9 pozycje: 1 - 99U, 2 - 39U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja10.txt"      # 53U
# filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja11.txt"      # 37U




data = loadtxt(filename)
data1 = -data[:,1]

# Clip out good data
yw1=data1

#Janek pozycja 1
# yw1=data1[:30000]

#Janek pozycja 2 część 1
# yw1=data1[:88000]
# yw1=data1[:30000]
# Janek pozycja 2 część 1
# yw1=data1[90000:]
# yw1=data1[90000:121000]

#Janek pozycja 3 część 1
# yw1=data1[:84500]
# yw1=data1[:30000]
#Janek pozycja 3 część 2
# yw1=data1[91000:165000]
# yw1=data1[91000:122000]
#Janek pozycja 3 część 3
# yw1=data1[174000:208000]
# yw1=data1[174000:205000]

#Janek pozycja 5
# yw1=data1[:32000]

#Janek pozycja 6
# yw1=data1[:35000]

#Janek pozycja 7
# yw1=data1[:34000]

#Janek pozycja 8 (8 część 1)
# yw1=data1[:115000]
# yw1=data1[:34000]


# Janek pozycja 9 (8 część 2)
# yw1=data1[116000:]
# yw1=data1[116000:152000]

#Janek pozycja 10
# yw1=data1[:36000]

#Janek pozycja 11
# yw1=data1[:35000]

#Filters
yw1= highFilter (yw1, Fs, lowFrequency=1)

yw1 = notchFitler(yw1, Fs, 50, 2.5)
yw1 = notchFitler(yw1, Fs, 100, 50)
#
yw1=lowFilter(yw1, Fs, 80)

y1=yw1

times = arange(len(y1))/Fs

#Plot timeseries for both signals

rpeaks1, average_final1, templates1 = peaksAndAveraged (y1, False)
ts_tmpl = np.linspace(0, 0.6, templates1.shape[1], endpoint=False)

print(templates1.shape[0])



#Ploty

plt.plot(times, y1)
plt.scatter(rpeaks1/1000, y1[rpeaks1])
plt.grid()
plt.show()

freqs, psd1 = powerSpectralDensity(yw1, Fs)
plt.loglog(freqs, psd1)
plt.grid()
plt.show()

for beat in range(0,templates1.shape[0]):
    plt.plot(ts_tmpl, templates1[beat,:], '#1f77b4')
plt.grid()
plt.show()

plt.figure(figsize=(6, 6))
plt.plot(ts_tmpl, average_final1)
# plt.grid()
plt.show()
