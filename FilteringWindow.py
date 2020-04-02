from biosppy.signals import ecg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from psd import *
from scipy import *
from scipy import signal
from scipy.signal import filtfilt
from tkinter import *
from tkinter import messagebox as m_box
matplotlib.use("TkAgg")


class FilteringWindowDesigner:

    def __init__(self, modificator, filtering_window):
        self.mdf = modificator
        self.mkg_designing(filtering_window)

    def mkg_designing(self, window):

        self.create_frames(window)
        self.fill_parameters_frame()
        self.fill_plot_frames()
        self.create_apply_button()
        self.first_run()
        self.create_average_label()

    def first_run(self):
        self.send_plot_frames()
        self.send_all_values_to_modification()

    def create_frames(self, window):
        self.filtersParFrame = Frame(window, bg='#b6d5d6', bd=10)
        self.filtersParFrame.place(relx=0, rely=0, relwidth=0.25, relheight=0.5)
        self.averageParFrame = Frame(window, bg='#b6d5d6', bd=0)
        self.averageParFrame.place(relx=0, rely=0.5, relwidth=0.25, relheight=0.5)

        back_frame = Frame(window, bg='#b6d5d6')
        back_frame.place(relx=0.25, rely=0, relwidth=0.77, relheight=1)

        self.signalPlotFrame = Frame(window, bg='#b6d5d6', bd=10)
        self.signalPlotFrame.place(relx=0.25, rely=0.01, relwidth=0.375, relheight=0.49)
        self.powerPlotFrame = Frame(window, bg='#b6d5d6', bd = 10)
        self.powerPlotFrame.place(relx=0.62, rely=0.01, relwidth=0.375, relheight=0.49)
        self.butterflyPlotFrame = Frame(window, bg='#b6d5d6', bd = 10)
        self.butterflyPlotFrame.place(relx=0.25, rely=0.49, relwidth=0.375, relheight=0.5)
        self.averagePlotFrame = Frame(window, bg='#b6d5d6', bd = 10)
        self.averagePlotFrame.place(relx=0.62, rely=0.49, relwidth=0.375, relheight=0.5)
        
    def fill_parameters_frame(self):
        filters_label = Label(self.filtersParFrame, text="Filtry: ", font='Times  20 bold')
        filters_label.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.2)

        self.create_filters_par()

        empty_space_end = Label(self.filtersParFrame).place(relx=0.02, rely=0.975, relwidth=0.96, relheight=0.025)

    def create_filters_par(self):
        self.hp_par_entries()
        self.lp_par_entries()
        self.bp_par_entries()

    def hp_par_entries(self):
        hp_check = Checkbutton(self.filtersParFrame, text="górnoprzepustowy:", font=("Helvetica", 11, "bold"),
                               anchor=CENTER, padx=15, variable=self.mdf.hpCheckVar)
        hp_check.var = self.mdf.hpCheckVar
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
        lp_check = Checkbutton(self.filtersParFrame, text="dolnoprzepustowy:", font=("Helvetica", 11, "bold"),
                               anchor=CENTER, padx=15, variable=self.mdf.lpCheckVar)
        lp_check.var = self.mdf.lpCheckVar
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
        bp_check = Checkbutton(self.filtersParFrame, text="środkowozaporowy: ", font=("Helvetica", 11, "bold"),
                               anchor=CENTER, padx=15, variable=self.mdf.bpCheckVar,
                               command=self.mdf.checkbox_change_state)
        bp_check.var = self.mdf.bpCheckVar
        bp_check.place(relx=0.02, rely=0.525, relwidth=0.96, relheight=0.1)
        bp_freq_label = Label(self.filtersParFrame, text="Częstotliwość środkowa", font='Helvetica 11')
        bp_freq_label.place(relx=0.02, rely=0.605, relwidth=0.48, relheight=0.065)
        bp_width_label = Label(self.filtersParFrame, text="Szerokość pasma", font='Helvetica 11')
        bp_width_label.place(relx=0.505, rely=0.605, relwidth=0.475, relheight=0.065)

        self.create_bp_entries()

    def create_bp_entries(self):
        n = 0
        for i in self.mdf.bpValues:
            self.mdf.bpDictionary[i] = {}
            bp_var = BooleanVar(value=True)
            self.mdf.bpDictionary[i]["Button"] = Checkbutton(self.filtersParFrame, text=f"{i} Hz".rjust(6, ' '),
                                                             font=("", 11), width=50, anchor=W, padx=50, variable=bp_var)
            self.mdf.bpDictionary[i]["Button"].var = bp_var
            self.mdf.bpDictionary[i]["Button"].select()
            self.mdf.bpDictionary[i]["Button"].place(relx=0.02, rely=0.675 + n, relwidth=0.48, relheight=0.05)
            self.mdf.bpDictionary[i]["Value"] = Entry(self.filtersParFrame, font=("", 11), justify=CENTER)
            self.mdf.bpDictionary[i]["Value"].place(relx=0.505, rely=0.675 + n, relwidth=0.37, relheight=0.05)
            bp_width = Label(self.filtersParFrame, font=("", 11), text="Hz")
            bp_width.place(relx=0.875, rely=0.675 + n, relwidth=0.105, relheight=0.05)
            if i == 150:
                n = n + .053
            else:
                n = n + .05
        self.mdf.set_bp_values()

    def create_average_label(self):
        heart_beats_label = Label(self.averageParFrame, text='Uśrednienie dla ' + self.mdf.heartBeatsQuantity +
                                                             ' cykli serca',font='20', bg='white')
        heart_beats_label.place(relx=0.2, rely=0.15, relwidth=0.6, relheight=0.1)

    def fill_plot_frames(self):
        signals_figure = Figure(figsize=(0.5, 0.5))
        ax1 = signals_figure.add_subplot(111)
        plot_signals = FigureCanvasTkAgg(signals_figure, self.signalPlotFrame)
        plot_signals.draw()
        plot_signals.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plot_signals, self.signalPlotFrame).update()
        plot_signals._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        power_figure = Figure(figsize=(0.5, 0.5))
        ax2 = power_figure.add_subplot(111)
        plot_power = FigureCanvasTkAgg(power_figure, self.powerPlotFrame)
        plot_power.draw()
        plot_power.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plot_power, self.powerPlotFrame).update()
        plot_power._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        butterfly_figure = Figure(figsize=(0.5, 0.5))
        ax3 = butterfly_figure.add_subplot(111)
        plot_butterfly = FigureCanvasTkAgg(butterfly_figure, self.butterflyPlotFrame)
        plot_butterfly.draw()
        plot_butterfly.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plot_butterfly, self.butterflyPlotFrame).update()
        plot_butterfly._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        average_figure = Figure(figsize=(0.5, 0.5))
        ax4 = average_figure.add_subplot(111)
        plot_average = FigureCanvasTkAgg(average_figure, self.averagePlotFrame)
        plot_average.draw()
        plot_average.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        NavigationToolbar2Tk(plot_average, self.averagePlotFrame).update()
        plot_average._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.ax = [ax1, ax2, ax3, ax4]
        self.plots = [plot_signals, plot_power, plot_butterfly, plot_average]

    def create_apply_button(self):
        apply_button = Button(self.averageParFrame, text="Zastosuj", command=self.send_all_values_to_modification,
                              font='Tahoma  15 bold', bg='white')
        apply_button.place(relx=0.2, rely=0.01, relwidth=0.6, relheight=0.1)

    def send_all_values_to_modification(self):

        hp_value = self.hpEntryValue.get()
        hp_order = self.hpOrderValue.get()

        lp_value = self.lpEntryValue.get()
        lp_order = self.lpOrderValue.get()

        self.mdf.set_all_values_and_modify(hp_value, hp_order, lp_value, lp_order)

    def send_plot_frames(self):
        self.mdf.get_plot_frames(self.ax, self.plots)


class FiltrationWindowDataModificator:

    def __init__(self, data, fs_value):

        self.data = data
        self.fsValue = fs_value
        self.hpCheckVar = BooleanVar(value=True)
        self.hpValue = 1.
        self.hpOrderValue = 5
        self.lpCheckVar = BooleanVar(value=True)
        self.lpValue = 150.
        self.lpOrderValue = 4
        self.bpCheckVar = BooleanVar(value=True)
        self.bpDictionary = {}
        self.bpValues = [50, 100, 150, 35, 45, 55]
        self.bpDefault50 = 4.
        self.bpDefault = 2.

    def set_bp_values(self):

        for x in self.bpDictionary.keys():
            if x == 50:
                self.bpDictionary[x]["Value"].insert(0, self.bpDefault50)
            else:
                self.bpDictionary[x]["Value"].insert(0, self.bpDefault)

    def checkbox_change_state(self):
        for x in self.bpDictionary.keys():
            if self.bpCheckVar.get():
                self.bpDictionary[x]["Button"].select()
            elif not self.bpCheckVar.get():
                self.bpDictionary[x]["Button"].deselect()

    def check_the_data_type(self):
        error_text = ""
        try:
            self.hpOrderValue = int(self.hpOrderValue)
            self.lpOrderValue = int(self.lpOrderValue)
        except ValueError:
            error_text = error_text + "► Rząd filtrów powinien być liczbą całkowitą\n"
        try:
            self.hpValue = float(self.hpValue)
            self.lpValue = float(self.lpValue)
        except ValueError:
            error_text = error_text + "► Częstotliwośc graniczna filtrów powinna być liczbą\n"
        try:
            for x in self.bpDictionary.keys():
                self.bpDictionary[x]["WidthValues"] = float(self.bpDictionary[x]["Value"].get())
        except ValueError:
            error_text = error_text + "► Szerokość pasma powinna być wyrażona liczbą\n"
        if error_text == "":
            return True
        else:
            m_box.showerror('Błędny typ danych', f'{error_text}\nWprowadż dane jeszcze raz!')
            return False

    def check_the_correctness(self):
        error_text = ""
        nyquist_frequency = self.fsValue / 2
        if self.hpCheckVar.get():
            if 0 < self.hpValue <= 4:
                high_order_limit = self.hpValue + 5
            elif 5 <= self.hpValue <= 7:
                high_order_limit = 9
            elif 8 <= self.hpValue <= 10:
                high_order_limit = 10
            elif 11 <= self.hpValue <= 14:
                high_order_limit = 11
            elif 14 <= self.hpValue <= 20:
                high_order_limit = 12
            else:
                high_order_limit = 12
                error_text = error_text + "► Wartość częstotliwości granicznej filtru \n    górnoprzepustowego " \
                                          "powinna mieścić się \n    w przedziale (0, 20] Hz\n "

            if self.hpOrderValue < 1 or self.hpOrderValue > high_order_limit:
                error_text = error_text + f"► Rząd filtru górnoprzepustowego znajduje się \n     poza dopuszczalnym " \
                                          f"przedziałem [1, {high_order_limit}]\n"
        if self.lpCheckVar.get():
            if self.lpValue <= self.hpValue or self.lpValue > 200:
                error_text = error_text + f"► Wartość częstotliwości granicznej filtru \n    dolnoprzepustowego " \
                                          f"powinna mieścić się \n    w przedziale ({self.hpValue}, " \
                                          f"{200}] Hz\n "
            high_order_limit = int(self.lpValue * 0.3)
            if self.lpOrderValue < 1 or self.lpOrderValue > high_order_limit:
                error_text = error_text + f"► Rząd filtru dolnoprzepustowego znajduje się \n     poza dopuszczalnym " \
                                          f"przedziałem [1, {high_order_limit}]\n"
        for x in self.bpDictionary.keys():
            if self.bpDictionary[x]["Button"].var.get():
                if self.bpDictionary[x]["WidthValues"] <= 0 or self.bpDictionary[x]["WidthValues"] >= nyquist_frequency:
                    error_text = error_text + f"► Szerokość pasma dla częstotliwości środkowej = {x} \n    filtru " \
                                              f"środkowozaporowego znajduje się poza \n    dopuszczalnym przedziałem " \
                                              f"(0, {nyquist_frequency}) Hz\n "
        if error_text == "":
            return True
        else:
            m_box.showerror('Błednie wprowadzone dane!', f'{error_text}\nWprowadż dane jeszcze raz!')
            return False

    def set_all_values_and_modify(self, hp_value, hp_order, lp_value, lp_order):
        self.hpValue = hp_value
        self.hpOrderValue = hp_order

        self.lpValue = lp_value
        self.lpOrderValue = lp_order

        if self.check_the_data_type() and self.check_the_correctness():
            self.modify_data()

    def get_plot_frames(self, ax, plots):
        self.ax = ax
        self.plots = plots

    def modify_data(self):
        self.modified_data = self.data
        if self.hpCheckVar.get():
            self.high_filter()
        if self.lpCheckVar.get():
            self.low_filter()
        for x in self.bpDictionary.keys():
            if self.bpDictionary[x]["Button"].var.get():
                bp_value = x
                width = float(self.bpDictionary[x]["Value"].get())
                self.notch_fitler(bp_value, width)
        rpeaks, average_final, templates = self.peaks_and_averaged()
        self.heartBeatsQuantity = str(templates.shape[0])
        self.modify_plots(rpeaks, average_final, templates)

    def high_filter(self):
        nyquist_frequency = self.fsValue / 2.
        normalized_cutoff = self.hpValue / nyquist_frequency
        b, a = signal.butter(self.hpOrderValue, normalized_cutoff, btype='high')
        self.modified_data = filtfilt(b, a, self.modified_data)

    def low_filter(self):
        nyquist_frequency = self.fsValue / 2.
        normalized_cutoff = self.lpValue / nyquist_frequency
        b, a = signal.butter(self.lpOrderValue, normalized_cutoff, btype='low')
        self.modified_data = filtfilt(b, a, self.modified_data)

    def notch_fitler(self, frequency, width):
        nyquist_frequency = self.fsValue / 2.
        normalized_cutoff = frequency / nyquist_frequency
        Q = frequency / width
        b, a = signal.iirnotch(w0=normalized_cutoff, Q=Q)
        self.modified_data = signal.filtfilt(b, a, self.modified_data)

    def modify_plots(self, rpeaks, average_final, templates):
        ts_tmpl = np.linspace(0, 0.7, templates.shape[1], endpoint=False)

        self.draw_signal(0, rpeaks)
        self.draw_power_spectral(1)
        self.draw_butterfly_plot(2, templates, ts_tmpl)
        self.draw_averaging_plot(3, average_final, ts_tmpl)

    def peaks_and_averaged (self):
        ecg_data = ecg.ecg(self.modified_data, sampling_rate=self.fsValue, show=False)
        rpeaks = ecg_data['rpeaks']
        templates = ecg_data['templates']
        average_final = np.average(templates, axis=0)
        return rpeaks, average_final, templates

    def draw_signal(self, figure_position, rpeaks):
        times = arange(len(self.modified_data)) / self.fsValue
        self.ax[figure_position].clear()
        self.ax[figure_position].set_title('Sygnał MKG', fontsize=12)
        self.ax[figure_position].set_xlabel('Czas [s]', fontsize=7, labelpad=0)
        self.ax[figure_position].set_ylabel('Amplituda [pT]', fontsize=7, labelpad=0)
        self.ax[figure_position].plot(times, self.modified_data)
        self.ax[figure_position].scatter(rpeaks/self.fsValue, self.modified_data[rpeaks], c='red')

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
        self.ax[figure_position].set_title('Przebieg ' + self.heartBeatsQuantity + ' cykli serca', fontsize=12)
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