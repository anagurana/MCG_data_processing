import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

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



class MKGAppDesigner:

    def __init__(self, modificator, filtering_window):
        self.modificator = modificator
        self.bpValues = [50, 100, 150, 35, 45, 55]
        self.hpDefaultValue = 1.
        self.lpDefaultValue = 150.
        self.bpDefault50 = 4.
        self.bpDefault = 2.
        self.dictionary = {}
        self.mkg_designing(filtering_window)

    def mkg_designing(self, window):

        s = ttk.Style()
        print(s.theme_names())
        s.theme_use('alt')
        self.create_frames(window)
        self.create_labels_and_entries()
        self.create_checkbuttons()
        self.create_plot_figures()
        self.create_apply_button()

        self.send_all_values()
        self.modificator.modify_data()

    def create_frames(self, window):
        self.filtersParFrame = Frame(window, bg='#b6d5d6')
        self.filtersParFrame.place(relx=0, rely=0, relwidth=0.3, relheight=0.5)
        self.averageParFrame = Frame(window, bg='#b6d5d6')
        self.averageParFrame.place(relx=0, rely=0.5, relwidth=0.3, relheight=0.5)

        backFrame = Frame(window, bg='#b6d5d6')
        backFrame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        self.signalPlotFrame = Frame(window, bg='#b6d5d6')
        self.signalPlotFrame.place(relx=0.3, rely=0.01, relwidth=0.347, relheight=0.49)
        self.powerPlotFrame = Frame(window, bg='#b6d5d6')
        self.powerPlotFrame.place(relx=0.647, rely=0.01, relwidth=0.347, relheight=0.49)
        self.butterflyPlotFrame = Frame(window, bg='#b6d5d6')
        self.butterflyPlotFrame.place(relx=0.3, rely=0.5, relwidth=0.347, relheight=0.49)
        self.averagePlotFrame = Frame(window, bg='#b6d5d6')
        self.averagePlotFrame.place(relx=0.647, rely=0.5, relwidth=0.347, relheight=0.49)

    def create_labels_and_entries(self):
        filtersLabel = Label(self.filtersParFrame, text="Filtry: ", font='Helvetica 18 bold')
        filtersLabel.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)

        fsLabel = Label(self.filtersParFrame, text="Częstotliwość próbkowania                            Hz", font='15',
                        justify=CENTER)
        fsLabel.place(relx=0.02, rely=0.12, relwidth=0.96, relheight=0.1)
        self.fsEntry = Entry(self.filtersParFrame, font='15', justify=CENTER)
        self.fsEntry.place(relx=0.65, rely=0.12, relwidth=0.15, relheight=0.1)
        self.fsEntry.insert(0, 1000)

        Label(self.averageParFrame, text="Uśrednienie dla", font='20').place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.1)
        self.heartBeats = Entry(self.averageParFrame, state="readonly", font='Helvetica 18 bold', justify = CENTER)
        self.heartBeats.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.1)
        Label(self.averageParFrame, text="cykli serca", font='20').place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.1)

    def create_checkbuttons(self):
        self.hpCheckVar = BooleanVar(value=True)
        hpCheck = Checkbutton(self.filtersParFrame, text="górnoprzepustowy:", font=15, anchor=W, padx=15, variable=self.hpCheckVar)
        hpCheck.var = self.hpCheckVar
        hpCheck.place(relx=0.02, rely=0.225, relwidth=0.5, relheight=0.1)
        hpCheckFs = Label(self.filtersParFrame, text="fs =   ", font=15, anchor=W, justify=RIGHT)
        hpCheckFs.place(relx=0.52, rely=0.225, relwidth=0.13, relheight=0.1)
        self.hpEntryValue = Entry(self.filtersParFrame, font=15, justify=CENTER)
        self.hpEntryValue.insert(0, self.hpDefaultValue)
        self.hpEntryValue.place(relx=0.65, rely=0.225, relwidth=0.22, relheight=0.1)
        hpHz = Label(self.filtersParFrame, text="Hz", font=15)
        hpHz.place(relx=0.87, rely=0.225, relwidth=0.11, relheight=0.1)

        self.lpCheckVar = BooleanVar(value=True)
        lpCheck = Checkbutton(self.filtersParFrame, text="dolnoprzepustowy:", font=15, anchor=W, padx=15, variable=self.lpCheckVar)
        lpCheck.var = self.lpCheckVar
        lpCheck.place(relx=0.02, rely=0.325, relwidth=0.5, relheight=0.1)
        lpCheckFs = Label(self.filtersParFrame, text="fs =   ", font=15, anchor=W, justify=RIGHT)
        lpCheckFs.place(relx=0.52, rely=0.325, relwidth=0.13, relheight=0.1)
        self.lpEntryValue = Entry(self.filtersParFrame, font=15, justify=CENTER)
        self.lpEntryValue.insert(0, self.lpDefaultValue)
        self.lpEntryValue.place(relx=0.65, rely=0.325, relwidth=0.22, relheight=0.1)
        lpHz = Label(self.filtersParFrame, text="Hz", font=15)
        lpHz.place(relx=0.87, rely=0.325, relwidth=0.11, relheight=0.1)

        bpCheckVar = BooleanVar(value=True)
        bpCheck = Checkbutton(self.filtersParFrame, text="środkowozaporowy: ", font=15, anchor=W, padx=15, variable=bpCheckVar,
                              command=lambda: self.modificator.checkbox_change_state(bpCheckVar))
        bpCheck.var = bpCheckVar
        bpCheck.place(relx=0.02, rely=0.43, relwidth=0.96, relheight=0.1)
        bpFreqLabel = Label(self.filtersParFrame, text="Częstotliwość środkowa fo", font='13')
        bpFreqLabel.place(relx=0.02, rely=0.525, relwidth=0.48, relheight=0.05)
        bpWidthLabel = Label(self.filtersParFrame, text="Szerokość pasma", font='13')
        bpWidthLabel.place(relx=0.505, rely=0.525, relwidth=0.475, relheight=0.05)

        self.create_bp_entries()

    def create_bp_entries(self):

        n = 0
        for i in self.bpValues:
            self.dictionary[i] = {}
            bpVar = BooleanVar(value=True)
            self.dictionary[i]["Button"] = Checkbutton(self.filtersParFrame, text=f"{i} Hz".rjust(6, ' '), font=("", 13), width=50,
                                                  anchor=W, padx=75, variable=bpVar)
            self.dictionary[i]["Button"].var = bpVar
            self.dictionary[i]["Button"].select()
            self.dictionary[i]["Button"].place(relx=0.02, rely=0.58 + n, relwidth=0.48, relheight=0.05)
            self.dictionary[i]["Value"] = Entry(self.filtersParFrame, font='13', justify=CENTER)
            self.dictionary[i]["Value"].place(relx=0.505, rely=0.58 + n, relwidth=0.37, relheight=0.05)
            bpWidth = Label(self.filtersParFrame, font='13', text="Hz")
            bpWidth.place(relx=0.875, rely=0.58 + n, relwidth=0.105, relheight=0.05)
            if i == 150:
                n = n + .053
            else:
                n = n + .05
        self.set_bp_values()

    def set_bp_values(self):

        for x in self.dictionary.keys():
            if x == 50:
                self.dictionary[x]["Value"].insert(0, self.bpDefault50)
            else:
                self.dictionary[x]["Value"].insert(0, self.bpDefault)
        return self.dictionary

    def create_plot_figures(self):
        signalsFigure = Figure(figsize=(0.5, 0.5))
        ax1 = signalsFigure.add_subplot(111)
        plotSignals = FigureCanvasTkAgg(signalsFigure, self.signalPlotFrame)
        plotSignals.draw()
        plotSignals.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plotSignals, self.signalPlotFrame).update()
        plotSignals._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        powerFigure = Figure(figsize=(0.5, 0.5))
        ax2 = powerFigure.add_subplot(111)
        plotPower = FigureCanvasTkAgg(powerFigure, self.powerPlotFrame)
        plotPower.draw()
        plotPower.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plotPower, self.powerPlotFrame).update()
        plotPower._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        butterflyFigure = Figure(figsize=(0.5, 0.5))
        ax3 = butterflyFigure.add_subplot(111)
        plotButterfly = FigureCanvasTkAgg(butterflyFigure, self.butterflyPlotFrame)
        plotButterfly.draw()
        plotButterfly.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plotButterfly, self.butterflyPlotFrame).update()
        plotButterfly._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        averageFigure = Figure(figsize=(0.5, 0.5))
        ax4 = averageFigure.add_subplot(111)
        plotAverage = FigureCanvasTkAgg(averageFigure, self.averagePlotFrame)
        plotAverage.draw()
        plotAverage.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plotAverage, self.averagePlotFrame).update()
        plotAverage._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.ax = [ax1, ax2, ax3, ax4]
        self.plots = [plotSignals, plotPower, plotButterfly, plotAverage]

    def create_apply_button(self):

        applyB = Button(self.averageParFrame, text="Zastosuj", font=15, command=self.send_all_values)
        applyB.place(relx=0.2, rely=0, relwidth=0.6, relheight=0.1)

    def send_all_values(self):

        fs = int(self.fsEntry.get())
        hpValue = float(self.hpEntryValue.get())
        hpCheck = self.hpCheckVar.get()
        lpValue = float(self.lpEntryValue.get())
        lpCheck = self.lpCheckVar.get()

        self.modificator.set_all_values(fs, hpValue, hpCheck, lpValue, lpCheck, self.dictionary,  self.ax, self.plots,
                                        self.heartBeats)


class MKGAppModificator:

    def __init__(self, data):

        self.data = data
        self.dictionary = {}


    def checkbox_change_state(self, bpCheckVar):
        for x in self.dictionary.keys():
            if bpCheckVar.get():
                self.dictionary[x]["Button"].select()
            elif not bpCheckVar.get():
                self.dictionary[x]["Button"].deselect()

    def set_all_values(self, fs, hpValue, hpCheck, lpValue, lpCheck, dictionary, ax, plots, heartBeats):
        self.fs = fs
        self.hpValue = hpValue
        self.hpCheck = hpCheck
        self.lpValue = lpValue
        self.lpCheck = lpCheck
        self.dictionary = dictionary
        self.ax = ax
        self.plots = plots
        self.heartBeats = heartBeats
        self.modify_data()

    def modify_data(self):

        self.modified_data = self.data
        if self.hpCheck:
            self.high_filter()
        if self.lpCheck:
            self.low_filter()
        for x in self.dictionary.keys():
            if self.dictionary[x]["Button"].var.get():
                bpValue = x
                width = float(self.dictionary[x]["Value"].get())
                self.notch_fitler(bpValue, width)
        self.modify_plots()

    def high_filter(self):
        nyquistFrequency = self.fs / 2.
        normalizedCutoff = self.hpValue / nyquistFrequency
        b, a = signal.butter(5, normalizedCutoff, btype='high')
        self.modified_data = filtfilt(b, a, self.modified_data)

    def low_filter(self):
        nyquistFrequency = self.fs / 2.
        normalizedCutoff = self.lpValue / nyquistFrequency
        b, a = signal.butter(5, normalizedCutoff, btype='low')
        self.modified_data =  filtfilt(b, a, self.modified_data)

    def notch_fitler(self, frequency, width):
        nyquistFrequency = self.fs / 2.
        normalizedCutoff = frequency / nyquistFrequency
        Q = frequency / width
        b, a = signal.iirnotch(w0=normalizedCutoff, Q=Q)
        self.modified_data = signal.filtfilt(b, a, self.modified_data)

    def modify_plots(self):

        rpeaks, average_final, templates = self.peaks_and_averaged(False)
        ts_tmpl = np.linspace(0, 0.7, templates.shape[1], endpoint=False)

        self.heartBeats.config(state=NORMAL)
        self.heartBeats.delete(0, END)
        self. heartBeats.insert(0, templates.shape[0])
        self.heartBeats.config(state="readonly")

        self.draw_signal(0, rpeaks)
        self.draw_power_spectral(1)
        self.draw_butterfly_plot(2, templates, ts_tmpl)
        self.draw_averaging_plot(3, average_final, ts_tmpl)

    def peaks_and_averaged (self, visibility):
        ecgData = ecg.ecg(self.modified_data, sampling_rate= self.fs, show = visibility)
        rpeaks = ecgData['rpeaks']
        templates = ecgData['templates']
        average_final = np.average(templates, axis=0)
        return rpeaks, average_final, templates

    def draw_signal(self, figure_position, rpeaks):
        times = arange(len(self.modified_data)) / self.fs
        self.ax[figure_position].clear()
        self.ax[figure_position].plot(times, self.modified_data)
        self.ax[figure_position].scatter(rpeaks/self.fs, self.modified_data[rpeaks], c='red')

        self.plots[figure_position].draw()

    def draw_power_spectral(self, figure_position):
        self.ax[figure_position].clear()
        freqs, psd1 = powerSpectralDensity(self.modified_data, self.fs)
        self.ax[figure_position].loglog(freqs, psd1, 'tab:orange')

        self.plots[figure_position].draw()

    def draw_butterfly_plot(self, figure_position, templates1, ts_tmpl):
        self.ax[figure_position].clear()
        for beat in range(0, templates1.shape[0]):
            self.ax[figure_position].plot(ts_tmpl, templates1[beat, :], 'tab:red')

        self.plots[figure_position].draw()

    def draw_averaging_plot(self, figure_position, average_final, ts_tmpl):

        self.ax[figure_position].clear()
        self.ax[figure_position].plot(ts_tmpl, average_final, 'tab:blue')

        self.plots[figure_position].draw()


def start_program(data):

    filtering_window = Tk()
    filtering_window.geometry("1500x800")

    moficator = MKGAppModificator(data)
    MKGAppDesigner(moficator, filtering_window)

    filtering_window.mainloop()

filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja4.txt"
data = loadtxt(filename)
data = data[:, 1] * -1
start_program(data)



