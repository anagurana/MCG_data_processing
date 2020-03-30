from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk

from scipy import *
from scipy import signal
from scipy.signal import lfilter, freqz, butter, filtfilt
from psd import *
from biosppy.signals import ecg
import numpy as np
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

# TODO:
#  2. All the entries should be proper values (Limits)
#  4. Check what is going on with fs_value
#  7. All variables in function must be lowercase
#  8. Label doesn't have justify


class MKGDesigner:

    def __init__(self, modificator, filtering_window):
        self.mdf = modificator
        self.mkg_designing(filtering_window)

    def mkg_designing(self, window):

        self.create_frames(window)
        self.fill_parameters_frame()
        self.fill_plot_frames()
        self.create_apply_button()

        self.send_plot_frames()

        self.mdf.modify_data()

        self.create_average_label()

    def create_frames(self, window):
        self.filtersParFrame = Frame(window, bg='#b6d5d6', bd=10)
        self.filtersParFrame.place(relx=0, rely=0, relwidth=0.25, relheight=0.5)
        self.averageParFrame = Frame(window, bg='#b6d5d6', bd=0)
        self.averageParFrame.place(relx=0, rely=0.5, relwidth=0.25, relheight=0.5)

        backFrame = Frame(window, bg='#b6d5d6')
        backFrame.place(relx=0.25, rely=0, relwidth=0.77, relheight=1)

        self.signalPlotFrame = Frame(window, bg='#b6d5d6', bd=10)
        self.signalPlotFrame.place(relx=0.25, rely=0.01, relwidth=0.375, relheight=0.49)
        self.powerPlotFrame = Frame(window, bg='#b6d5d6', bd = 10)
        self.powerPlotFrame.place(relx=0.62, rely=0.01, relwidth=0.375, relheight=0.49)
        self.butterflyPlotFrame = Frame(window, bg='#b6d5d6', bd = 10)
        self.butterflyPlotFrame.place(relx=0.25, rely=0.49, relwidth=0.375, relheight=0.5)
        self.averagePlotFrame = Frame(window, bg='#b6d5d6', bd = 10)
        self.averagePlotFrame.place(relx=0.62, rely=0.49, relwidth=0.375, relheight=0.5)
        
    def create_fs_field(self):
        fsLabel = Label(self.filtersParFrame, text="Częstotliwość próbkowania", font='15', anchor = W, padx=20)
        fsLabel.place(relx=0.02, rely=0.12, relwidth=0.85, relheight=0.1)
        self.fsEntry = Entry(self.filtersParFrame, font='15', justify=CENTER)
        self.fsEntry.place(relx=0.65, rely=0.135, relwidth=0.22, relheight=0.07)
        self.fsEntry.insert(0, self.mdf.fsValue)
        fsLabel = Label(self.filtersParFrame, text="Hz", font='15', justify=LEFT)
        fsLabel.place(relx=0.87, rely=0.12, relwidth=0.11, relheight=0.1)
        
    def hp_par_entries(self):
        self.hpCheckVar = BooleanVar(value=True)
        hp_check = Checkbutton(self.filtersParFrame, text="górnoprzepustowy:", font=15, anchor=CENTER, padx=15,
                              variable=self.hpCheckVar)
        hp_check.var = self.hpCheckVar
        hp_check.place(relx=0.02, rely=0.225, relwidth=0.96, relheight=0.1)

        hp_order_label = Label(self.filtersParFrame, text="rząd", font=("", 11), anchor=CENTER)
        hp_order_label.place(relx=0.02, rely=0.325, relwidth=0.145, relheight=0.05)
        self.hpOrderValue = Entry(self.filtersParFrame, font=("", 11), justify=CENTER)
        self.hpOrderValue.insert(0, self.mdf.hpOrderValue)
        self.hpOrderValue.place(relx=0.165, rely=0.325, relwidth=0.22, relheight=0.05)
        empty_label = Label(self.filtersParFrame).place(relx=0.385, rely=0.325, relwidth=0.113, relheight=0.05)

        hp_fs_label = Label(self.filtersParFrame, text="fs", font=("", 11), anchor=CENTER)
        hp_fs_label.place(relx=0.5, rely=0.325, relwidth=0.15, relheight=0.05)
        self.hpEntryValue = Entry(self.filtersParFrame, font=("", 11), justify=CENTER)
        self.hpEntryValue.insert(0, self.mdf.hpValue)
        self.hpEntryValue.place(relx=0.65, rely=0.325, relwidth=0.22, relheight=0.05)
        hp_hz_label = Label(self.filtersParFrame, text=" Hz", font=("", 11))
        hp_hz_label.place(relx=0.87, rely=0.325, relwidth=0.11, relheight=0.05)

    def lp_par_entries(self):
        self.lpCheckVar = BooleanVar(value=True)
        lp_check = Checkbutton(self.filtersParFrame, text="dolnoprzepustowy:", font=15, anchor=CENTER, padx=15,
                              variable=self.lpCheckVar)
        lp_check.var = self.lpCheckVar
        lp_check.place(relx=0.02, rely=0.375, relwidth=0.96, relheight=0.1)

        lp_order_label = Label(self.filtersParFrame, text="rząd", font=("", 11), anchor=CENTER)
        lp_order_label.place(relx=0.02, rely=0.475, relwidth=0.145, relheight=0.05)
        self.lpOrderValue = Entry(self.filtersParFrame, font=("", 11), justify=CENTER)
        self.lpOrderValue.insert(0, self.mdf.lpOrderValue)
        self.lpOrderValue.place(relx=0.165, rely=0.475, relwidth=0.22, relheight=0.05)
        empty_label=Label(self.filtersParFrame).place(relx=0.385, rely=0.475, relwidth=0.113, relheight=0.05)

        lp_fs_label = Label(self.filtersParFrame, text="fs", font=("", 11), anchor=CENTER)
        lp_fs_label.place(relx=0.5, rely=0.475, relwidth=0.15, relheight=0.05)
        self.lpEntryValue = Entry(self.filtersParFrame, font=("", 11), justify=CENTER)
        self.lpEntryValue.insert(0, self.mdf.lpValue)
        self.lpEntryValue.place(relx=0.65, rely=0.475, relwidth=0.22, relheight=0.05)
        lp_hz_label = Label(self.filtersParFrame, text=" Hz", font=("", 11))
        lp_hz_label.place(relx=0.87, rely=0.475, relwidth=0.11, relheight=0.05)

    def bp_par_entries(self):
        bpCheckVar = BooleanVar(value=True)
        bp_check = Checkbutton(self.filtersParFrame, text="środkowozaporowy: ", font=15, anchor=CENTER, padx=15,
                              variable=bpCheckVar,
                              command=lambda: self.mdf.checkbox_change_state(bpCheckVar))
        bp_check.var = bpCheckVar
        bp_check.place(relx=0.02, rely=0.525, relwidth=0.96, relheight=0.1)
        bpFreqLabel = Label(self.filtersParFrame, text="Częstotliwość środkowa", font='Helvetica 11')
        bpFreqLabel.place(relx=0.02, rely=0.625, relwidth=0.48, relheight=0.05)
        bpWidthLabel = Label(self.filtersParFrame, text="Szerokość pasma", font='Helvetica 11')
        bpWidthLabel.place(relx=0.505, rely=0.625, relwidth=0.475, relheight=0.05)

        self.create_bp_entries()

    def create_filters_par(self):
        self.hp_par_entries()
        self.lp_par_entries()
        self.bp_par_entries()

    def fill_parameters_frame(self):
        filtersLabel = Label(self.filtersParFrame, text="Filtry: ", font='Helvetica 18 bold underline')
        filtersLabel.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
    
        self.create_fs_field()
        self.create_filters_par()

        empty_space_end = Label(self.filtersParFrame).place(relx=0.02, rely=0.98, relwidth=0.96, relheight=0.02)

    def create_average_label(self):
        heart_beats_label = Label(self.averageParFrame, text='Uśrednienie dla ' + self.mdf.heart_beats_quantity + ' cykli '
                                                                                                          'serca',
                                  font='20', bg='white')
        heart_beats_label.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.1)

    def create_bp_entries(self):

        n = 0
        for i in self.mdf.bpValues:
            self.mdf.dictionary[i] = {}
            bpVar = BooleanVar(value=True)
            self.mdf.dictionary[i]["Button"] = Checkbutton(self.filtersParFrame, text=f"{i} Hz".rjust(6, ' '),
                                                           font=("", 11), width=50, anchor=W, padx=50, variable=bpVar)
            self.mdf.dictionary[i]["Button"].var = bpVar
            self.mdf.dictionary[i]["Button"].select()
            self.mdf.dictionary[i]["Button"].place(relx=0.02, rely=0.675 + n, relwidth=0.48, relheight=0.05)
            self.mdf.dictionary[i]["Value"] = Entry(self.filtersParFrame, font=("", 11), justify=CENTER)
            self.mdf.dictionary[i]["Value"].place(relx=0.505, rely=0.675 + n, relwidth=0.37, relheight=0.05)
            bp_width = Label(self.filtersParFrame, font=("", 11), text="Hz")
            bp_width.place(relx=0.875, rely=0.675 + n, relwidth=0.105, relheight=0.05)
            if i == 150:
                n = n + .053
            else:
                n = n + .05
        self.mdf.set_bp_values()

    def fill_plot_frames(self):
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

        # applyB = ttk.Button(self.averageParFrame, text="Zastosuj", command=self.send_all_values_to_modification)
        applyB = Button(self.averageParFrame, text="Zastosuj", command=self.send_all_values_to_modification, font='Tahoma  15 bold', bg='white')
        applyB.place(relx=0.2, rely=0.01, relwidth=0.6, relheight=0.1)

    def send_all_values_to_modification(self):

        fs = int(self.fsEntry.get())
        hp_check = self.hpCheckVar.get()
        hp_value = float(self.hpEntryValue.get())
        hp_order = int(self.hpOrderValue.get())

        lp_check = self.lpCheckVar.get()
        lp_value = float(self.lpEntryValue.get())
        lp_order = int(self.lpOrderValue.get())

        self.mdf.set_all_values(fs, hp_check, hp_value, hp_order, lp_check, lp_value, lp_order)
        self.mdf.modify_data()

    def send_plot_frames(self):
        self.mdf.get_plot_frames(self.ax, self.plots)


class DataModificator:

    def __init__(self, data, initial_fs):

        self.data = data
        self.dictionary = {}
        self.fsValue = 1000
        self.hpValue = 1.
        self.lpValue = 150.
        self.hpOrderValue = 5
        self.lpOrderValue = 4
        self.bpValues = [50, 100, 150, 35, 45, 55]
        self.bpDefault50 = 4.
        self.bpDefault = 2.
        self.hpCheck = True
        self.lpCheck = True
        self.initialFs = initial_fs

    def set_bp_values(self):

        for x in self.dictionary.keys():
            if x == 50:
                self.dictionary[x]["Value"].insert(0, self.bpDefault50)
            else:
                self.dictionary[x]["Value"].insert(0, self.bpDefault)

    def checkbox_change_state(self, bpCheckVar):
        for x in self.dictionary.keys():
            if bpCheckVar.get():
                self.dictionary[x]["Button"].select()
            elif not bpCheckVar.get():
                self.dictionary[x]["Button"].deselect()

    def set_all_values(self, fs, hp_check, hp_value, hp_order, lp_check, lp_value, lp_order):
        self.fsValue = fs

        self.hpCheck = hp_check
        self.hpValue = hp_value
        self.hpOrderValue = hp_order

        self.lpCheck = lp_check
        self.lpValue = lp_value
        self.lpOrderValue = lp_order

    def get_plot_frames(self, ax, plots):
        self.ax = ax
        self.plots = plots

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
        rpeaks, average_final, templates = self.peaks_and_averaged(visibility=False)
        self.heart_beats_quantity = str(templates.shape[0])
        self.modify_plots(rpeaks, average_final, templates)

    def high_filter(self):
        nyquistFrequency = self.fsValue / 2.
        normalizedCutoff = self.hpValue / nyquistFrequency
        b, a = signal.butter(self.hpOrderValue, normalizedCutoff, btype='high')
        self.modified_data = filtfilt(b, a, self.modified_data)

    def low_filter(self):
        nyquistFrequency = self.fsValue / 2.
        normalizedCutoff = self.lpValue / nyquistFrequency
        b, a = signal.butter(self.lpOrderValue, normalizedCutoff, btype='low')
        self.modified_data =  filtfilt(b, a, self.modified_data)

    def notch_fitler(self, frequency, width):
        nyquistFrequency = self.fsValue / 2.
        normalizedCutoff = frequency / nyquistFrequency
        Q = frequency / width
        b, a = signal.iirnotch(w0=normalizedCutoff, Q=Q)
        self.modified_data = signal.filtfilt(b, a, self.modified_data)

    def modify_plots(self, rpeaks, average_final, templates):
        ts_tmpl = np.linspace(0, 0.7, templates.shape[1], endpoint=False)

        self.draw_signal(0, rpeaks)
        self.draw_power_spectral(1)
        self.draw_butterfly_plot(2, templates, ts_tmpl)
        self.draw_averaging_plot(3, average_final, ts_tmpl)

    def peaks_and_averaged (self, visibility):
        ecgData = ecg.ecg(self.modified_data, sampling_rate=self.initialFs, show=visibility)
        rpeaks = ecgData['rpeaks']
        templates = ecgData['templates']
        average_final = np.average(templates, axis=0)
        return rpeaks, average_final, templates

    def draw_signal(self, figure_position, rpeaks):
        times = arange(len(self.modified_data)) / self.initialFs
        self.ax[figure_position].clear()
        self.ax[figure_position].set_title('Sygnał MKG', fontsize=12)
        self.ax[figure_position].set_xlabel('Czas [s]', fontsize=7, labelpad=0)
        self.ax[figure_position].set_ylabel('Amplituda [pT]', fontsize=7, labelpad=0)
        self.ax[figure_position].plot(times, self.modified_data)
        self.ax[figure_position].scatter(rpeaks/self.initialFs, self.modified_data[rpeaks], c='red')

        self.plots[figure_position].draw()

    def draw_power_spectral(self, figure_position):
        self.ax[figure_position].clear()
        self.ax[figure_position].set_title('Widmo mocy', fontsize=12)
        self.ax[figure_position].set_xlabel('Częstotliwość [Hz]', fontsize=7, labelpad=0)
        self.ax[figure_position].set_ylabel('Amplituda [pT]', fontsize=7, labelpad=3)
        freqs, psd1 = powerSpectralDensity(self.modified_data, self.fsValue)
        self.ax[figure_position].loglog(freqs, psd1)

        self.plots[figure_position].draw()

    def draw_butterfly_plot(self, figure_position, templates, ts_tmpl):
        self.ax[figure_position].clear()
        self.ax[figure_position].set_title('Przebieg ' + self.heart_beats_quantity + ' cykli serca', fontsize=12)
        self.ax[figure_position].set_xlabel('Czas [s]', fontsize=7, labelpad=0)
        self.ax[figure_position].set_ylabel('Amplituda [pT]', fontsize=7, labelpad=0)
        for beat in range(0, templates.shape[0]):
            self.ax[figure_position].plot(ts_tmpl, templates[beat, :], 'tab:red')

        self.plots[figure_position].draw()

    def draw_averaging_plot(self, figure_position, average_final, ts_tmpl):

        self.ax[figure_position].clear()
        self.ax[figure_position].set_title('Uśredniony sygnał MKG', fontsize=12)
        self.ax[figure_position].set_xlabel('Czas [s]', fontsize=7, labelpad=0)
        self.ax[figure_position].set_ylabel('Amplituda [pT]', fontsize=7, labelpad=0)
        self.ax[figure_position].plot(ts_tmpl, average_final, 'tab:red')

        self.plots[figure_position].draw()


def start_program(window, data, initial_fs):

    # window = tk.ThemedTk()
    # print(window.get_themes())
    # window.set_theme('plastik')
    # window.geometry("1500x800")

    modificator = DataModificator(data, initial_fs)
    MKGDesigner(modificator, window)

window = Tk()
window.geometry("1500x800")
filename = "Mapowanie+potencjaly_wylowane/mkg_janek_pozycja4.txt"
data = loadtxt(filename)
data = data[:, 1] *(-1)
initial_fs = 1000
start_program(window, data, initial_fs)
window.mainloop()



