import tkinter as tk
from tkinter import *
from tkinter import filedialog

from scipy import *
from scipy import signal
from scipy.signal import lfilter, freqz, butter, filtfilt
from psd import *
import matplotlib.pyplot as plt
from biosppy.signals import ecg
import numpy as np
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")


#TODO: 1. Add peaks
# 2. Averaging for
# 3. Add labels to bp Values


def create_filtration_window(data):
    filtering_window = Tk()
    filtering_window.geometry("1500x800")

    parFrames, plotFrames = create_frames(filtering_window)
    fsEntry, heartBeats = create_entries(parFrames)
    checkValues, dictionary, passbandEntry = create_checkbuttons(parFrames[0])
    figures, plots = create_plot_figures(plotFrames)
    create_apply_button(parFrames[1], data, fsEntry, passbandEntry, checkValues, dictionary, figures, plots, heartBeats)
    # think about it
    modify_plots(data, fsEntry, passbandEntry, checkValues, dictionary, figures, plots, heartBeats)

    filtering_window.mainloop()
def create_frames(filtering_window):

    filtersParF = Frame(filtering_window, bg='#3c9162', )
    filtersParF.place(relx=0.01, rely=0.01, relwidth=0.3, relheight=0.5)
    signalPlotF = Frame(filtering_window)
    signalPlotF.place(relx=0.31, rely=0.01, relwidth=0.34, relheight=0.49)
    powerPlotF = Frame(filtering_window)
    powerPlotF.place(relx=0.65, rely=0.01, relwidth=0.34, relheight=0.49)
    averageParF = Frame(filtering_window, bg='#3c9162')
    averageParF.place(relx=0.01, rely=0.5, relwidth=0.3, relheight=0.5)
    butterflyPlotF = Frame(filtering_window)
    butterflyPlotF.place(relx=0.31, rely=0.5, relwidth=0.34, relheight=0.49)
    averagePlotF = Frame(filtering_window)
    averagePlotF.place(relx=0.65, rely=0.5, relwidth=0.34, relheight=0.49)

    parFrames = [filtersParF, averageParF]
    plotFrames = [signalPlotF, powerPlotF, butterflyPlotF, averagePlotF]

    return parFrames, plotFrames
def create_entries(parFrames):

    filtersLabel = Label(parFrames[0], text="Filtry: ", font='Helvetica 18 bold')
    filtersLabel.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)

    fsLabel = Label(parFrames[0], text="Częstotliwość próbkowania                            Hz", font='15',
                    justify=CENTER)
    fsLabel.place(relx=0.02, rely=0.12, relwidth=0.96, relheight=0.1)
    fsEntry = Entry(parFrames[0], font='15', justify=CENTER)
    fsEntry.place(relx=0.65, rely=0.12, relwidth=0.15, relheight=0.1)
    fsEntry.insert(0, 1000)

    Label(parFrames[1], text="Uśrednienie dla                 cykli serca", font='20').place(relx=0.02, rely=0.45,
                                                                                            relwidth=0.96,
                                                                                            relheight=0.1)
    heartBeats = Entry(parFrames[1], state="readonly", font='Helvetica 18 bold', justify = CENTER)
    heartBeats.place(relx=0.5, rely=0.45, relwidth=0.1, relheight=0.1)

    return fsEntry, heartBeats
def create_checkbuttons(frame):

    hpVar = BooleanVar(value=True)
    hpCheck = Checkbutton(frame, text="górnoprzepustowy:", font=15, anchor=W, padx=15, variable=hpVar)
    hpCheck.var = hpVar
    hpCheck.place(relx=0.02, rely=0.225, relwidth=0.5, relheight=0.1)
    hpCheckFs = Label(frame, text="fs =   ", font=15, anchor=W, justify=RIGHT)
    hpCheckFs.place(relx=0.52, rely=0.225, relwidth=0.13, relheight=0.1)
    hpValue = Entry(frame, font=15, justify=CENTER)
    hpValue.insert (0, 1)
    hpValue.place(relx=0.65, rely=0.225, relwidth=0.22, relheight=0.1)
    hpHz = Label(frame, text="Hz", font=15)
    hpHz.place(relx=0.87, rely=0.225, relwidth=0.11, relheight=0.1)

    lpVar = BooleanVar(value=True)
    lpCheck = Checkbutton(frame, text="dolnoprzepustowy:", font=15, anchor=W, padx=15, variable=lpVar)
    lpCheck.var = lpVar
    lpCheck.place(relx=0.02, rely=0.325, relwidth=0.5, relheight=0.1)
    lpCheckFs = Label(frame, text="fs =   ", font=15, anchor=W, justify=RIGHT)
    lpCheckFs.place(relx=0.52, rely=0.325, relwidth=0.13, relheight=0.1)
    lpValue = Entry(frame, font=15, justify=CENTER)
    lpValue.insert(0, 150)
    lpValue.place(relx=0.65, rely=0.325, relwidth=0.22, relheight=0.1)
    lpHz = Label(frame, text="Hz", font=15)
    lpHz.place(relx=0.87, rely=0.325, relwidth=0.11, relheight=0.1)

    bpVar = BooleanVar(value=True)
    bpCheck = Checkbutton(frame, text="środkowozaporowy: ", font=15, anchor=W, padx=15, variable=bpVar, command=lambda: global_change_state(bpVar, dictionary))
    bpCheck.var = bpVar
    bpCheck.place(relx=0.02, rely=0.43, relwidth=0.96, relheight=0.1)
    bpFreqLabel = Label(frame, text="Częstotliwość środkowa fo", font='13')
    bpFreqLabel.place(relx=0.02, rely=0.525, relwidth=0.48, relheight=0.05)
    bpWidthLabel = Label(frame, text="Szerokość pasma", font='13')
    bpWidthLabel.place(relx=0.505, rely=0.525, relwidth=0.475, relheight=0.05)

    checkValues = [hpVar, lpVar]
    passband = [hpValue, lpValue]
    bpValues = [50, 100, 150, 35, 45, 55]
    dictionary = create_BP_entries(bpValues, frame, bpCheck)
    dictionary = set_bp_values(dictionary)
    return checkValues, dictionary, passband
def global_change_state(bpVar, dictionary):
    for x in dictionary.keys():
        if bpVar.get():
            dictionary[x]["Button"].select()
        elif not bpVar.get():
            dictionary[x]["Button"].deselect()
def changing_states(dictionary, bpCheck):
    for x in dictionary.keys():
        if dictionary[x]["Button"].var.get():
            bpCheck.select()
        else:
            bpCheck.deselect()
def create_BP_entries(bpValues, filtersParF, bpCheck):
    dictionary = {}
    n = 0
    for i in bpValues:
        dictionary[i] = {}
        var = BooleanVar(value=True)
        dictionary[i]["Button"] = Checkbutton(filtersParF, text=f"{i} Hz".rjust(6, ' '), font=("", 13), width = 50, anchor = W, padx=75, variable = var)
        dictionary[i]["Button"].var = var
        dictionary[i]["Button"].select()
        dictionary[i]["Button"].place(relx=0.02, rely=0.58+n, relwidth=0.48, relheight=0.05)
        dictionary[i]["Value"] = Entry(filtersParF, font='13', justify = CENTER)
        dictionary[i]["Value"].place(relx=0.505, rely=0.58+n, relwidth=0.37, relheight=0.05)
        bpWidth = Label(filtersParF, font='13', text="Hz")
        bpWidth.place(relx=0.875, rely=0.58+n, relwidth=0.105, relheight=0.05)
        if i == 150:
            n=n+.053
        else:
            n = n+.05
    return dictionary
def set_bp_values(dictionary):

    for x in dictionary.keys():
        if x == 50:
            bp50 = dictionary[x]["DefaultValue"] = 4
            dictionary[x]["Value"].insert(0, bp50)
        else:
            bpAll = dictionary[x]["DefaultValue"] = 2
            dictionary[x]["Value"].insert(0, bpAll)
    return dictionary
def create_plot_figures(plotFrames):
    signalsFigure = Figure(figsize=(0.5, 0.5))
    ax1 = signalsFigure.add_subplot(111)
    plotSignals = FigureCanvasTkAgg(signalsFigure, plotFrames[0])
    plotSignals.draw()
    plotSignals.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    NavigationToolbar2Tk(plotSignals, plotFrames[0]).update
    plotSignals._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    powerFigure = Figure(figsize=(0.5, 0.5))
    ax2 = powerFigure.add_subplot(111)
    plotPower = FigureCanvasTkAgg(powerFigure, plotFrames[1])
    plotPower.draw()
    plotPower.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    NavigationToolbar2Tk(plotPower, plotFrames[1]).update()
    plotPower._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    butterflyFigure = Figure(figsize=(0.5, 0.5))
    ax3 = butterflyFigure.add_subplot(111)
    plotButterfly = FigureCanvasTkAgg(butterflyFigure, plotFrames[2])
    plotButterfly.draw()
    plotButterfly.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    NavigationToolbar2Tk(plotButterfly, plotFrames[2]).update()
    plotButterfly._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    averageFigure = Figure(figsize=(0.5, 0.5))
    ax4 = averageFigure.add_subplot(111)
    plotAverage = FigureCanvasTkAgg(averageFigure, plotFrames[3])
    plotAverage.draw()
    plotAverage.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    NavigationToolbar2Tk(plotAverage, plotFrames[3]).update()
    plotAverage._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    figures = [ax1, ax2, ax3, ax4]
    plots = [plotSignals, plotPower, plotButterfly, plotAverage]

    return figures, plots
def create_apply_button(frame, data, fsEntry, passbandEntry, checkValues, dictionary, figures, plots,heartBeats):
    applyB = Button(frame, text="Zastosuj", font=15, command=lambda: modify_plots(data, fsEntry, passbandEntry, checkValues, dictionary, figures, plots,heartBeats))
    applyB.place(relx=0.2, rely=0.02, relwidth=0.6, relheight=0.1)
def highFilter(data, Fs, lowFrequency ):
    nyquistFrequency = Fs / 2.
    normalizedCutoff = lowFrequency / nyquistFrequency
    b, a = signal.butter(5, normalizedCutoff, btype='high')
    return filtfilt(b, a, data)
def lowFilter(data, Fs, highFrequency):
    nyquistFrequency = Fs / 2.
    normalizedCutoff = highFrequency / nyquistFrequency
    b,a = signal.butter(5, normalizedCutoff, btype='low')
    return filtfilt(b, a, data)
def notchFitler(data, Fs, frequency, width):
    nyquistFrequency = Fs/2.
    normalizedCutoff = frequency/nyquistFrequency
    Q = frequency/width
    b,a = signal.iirnotch(w0=normalizedCutoff, Q=Q)
    xfiltered = signal.filtfilt(b,a,data)
    return xfiltered
def modify_data(data, Fs, passbandEntry, checkValues, dictionary):

    if checkValues[0].get():
        hpValue = float(passbandEntry[0].get())
        data = highFilter(data, Fs, hpValue)
    if checkValues[1].get():
        lpValue = float(passbandEntry[1].get())
        data = lowFilter(data, Fs, lpValue)
    for x in dictionary.keys():
        if dictionary[x]["Button"].var.get():
            bpValue = x
            width = int(dictionary[x]["Value"].get())
            data = notchFitler(data, Fs, bpValue, width)

    return data
def modify_plots(data, fsEntry, passbandEntry, checkValues, dictionary, figures, plots,heartBeats):
    Fs = int(fsEntry.get())
    modified_data = modify_data(data, Fs, passbandEntry, checkValues, dictionary)

    rpeaks, average_final, templates = peaksAndAveraged(modified_data, Fs, False)
    ts_tmpl = np.linspace(0, 0.7, templates.shape[1], endpoint=False)
    heartBeats.config(state=NORMAL)
    heartBeats.delete(0, END)
    heartBeats.insert(0, templates.shape[0])
    heartBeats.config(state = "readonly")

    draw_signal(modified_data, Fs, rpeaks, figures[0], plots[0])
    draw_power_spectral(modified_data, Fs, figures[1], plots[1])
    draw_butterfly_plot(templates, ts_tmpl, figures[2], plots[2])
    draw_averaging_plot(average_final, ts_tmpl, figures[3], plots[3])
def draw_signal(data, Fs, rpeaks, mainFigure, drawn_plot):
    times = arange(len(data)) / Fs
    mainFigure.clear()
    mainFigure.plot(times, data)
    mainFigure.scatter(rpeaks/ 1000, data[rpeaks], c='red')

    drawn_plot.draw()
def draw_power_spectral(data, Fs,  mainFigure, drawn_plot):
    mainFigure.clear()
    freqs, psd1 = powerSpectralDensity(data, Fs)
    mainFigure.loglog(freqs, psd1, 'tab:orange')
    drawn_plot.draw()
def peaksAndAveraged (signal, Fs, visibility):
    ecgData = ecg.ecg(signal, sampling_rate= Fs, show = visibility)
    rpeaks = ecgData['rpeaks']
    templates = ecgData['templates']
    average_final = np.average(templates, axis=0)
    return rpeaks, average_final, templates
def draw_butterfly_plot(templates1, ts_tmpl, mainFigure, drawn_plot ):
    mainFigure.clear()
    for beat in range(0, templates1.shape[0]):
        mainFigure.plot(ts_tmpl, templates1[beat, :], 'tab:red')
    drawn_plot.draw()
def draw_averaging_plot(average_final, ts_tmpl, mainFigure, drawn_plot ):

    mainFigure.clear()
    mainFigure.plot(ts_tmpl, average_final, 'tab:blue')
    drawn_plot.draw()


def main ():
    filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja4.txt"
    data = loadtxt(filename)
    data=data[:, 1]*-1
    create_filtration_window(data)

main()

