import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as m_box

from MKG_app import start_program

from scipy import *
import numpy as np
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")


class AppDesigner:
    def __init__(self, modificator, window):
        self.window = window
        self.modificator = modificator
        self.window_designing()

    def window_designing(self):
        self.create_frames()
        self.design_par_frame()
        self.design_plot_frame()
        self.send_plot_frames()
        self.design_open_frame()

    def create_frames(self):

        self.fileFrame = LabelFrame(self.window)
        self.fileFrame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.plotFrame = Frame(self.window)
        self.plotFrame.place(relx=0, rely=0.1, relwidth=1, relheight=0.7)
        self.modFrame = Frame(self.window, bg='#b6d5d6')
        self.modFrame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)

    def design_par_frame(self):

        self.create_labels_and_entries()
        self.create_buttons()

    def create_labels_and_entries(self):
        scalingL = Label(self.modFrame, text="Współczynnik skalowania", font=15)
        scalingL.place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.2)
        self.scalingRateEntry = Entry(self.modFrame, font=15, justify=CENTER, state = 'readonly')
        self.scalingRateEntry.place(relx=0.25, rely=0.3, relwidth=0.2, relheight=0.2)

        lengthL = Label(self.modFrame, text="Długość", font=15)
        lengthL.place(relx=0.05, rely=0.5, relwidth=0.2, relheight=0.2)
        self.lengthFrom = Entry(self.modFrame, font=15, justify=CENTER, state = 'readonly')
        self.lengthFrom.place(relx=0.25, rely=0.5, relwidth=0.085, relheight=0.2)
        lengthLabel = Label(self.modFrame, text=" : ", font=15)
        lengthLabel.place(relx=0.335, rely=0.5, relwidth=0.01, relheight=0.2)
        self.lengthTo = Entry(self.modFrame, font=15, justify=CENTER, state = 'readonly')
        self.lengthTo.place(relx=0.345, rely=0.5, relwidth=0.085, relheight=0.2)
        sLabel = Label(self.modFrame, text="s", font=15)
        sLabel.place(relx=0.43, rely=0.5, relwidth=0.02, relheight=0.2)

    def create_buttons(self):
        self.applyButton = Button(self.modFrame, text="Zastosuj", font='Tahoma  16 bold', state = DISABLED, bg="white",
                                  command=self.send_modified_data)
        self.applyButton.place(relx=0.5, rely=0.3, relwidth=0.2, relheight=0.4)
        self.nextButton = Button(self.modFrame, text="Przejdź do filtracji   →", font='Tahoma 16 bold', state=DISABLED,
                                 bg="white", command=self.open_filtration_window)
        self.nextButton.place(relx=0.75, rely=0.3, relwidth=0.2, relheight=0.4)

    def design_open_frame(self):
        initial_fs_label = Label(self.fileFrame, text="Częstotliwość próbkowania sygnału", font=15,  borderwidth=2,
                                 relief="ridge", anchor="w", padx = 6, bg="#dfeff0")
        initial_fs_label.place(relx=0.05, rely=0.2, relwidth=0.31, relheight=0.6)
        initial_fs = Entry(self.fileFrame, font=15, justify = CENTER)
        initial_fs.place(relx=0.23, rely=0.3, relwidth=0.1, relheight=0.4)
        hz_label = Label(self.fileFrame, font=15, text="Hz", bg="#dfeff0")
        hz_label.place(relx=0.33, rely=0.3, relwidth=0.029, relheight=0.4)

        button = Button(self.fileFrame, text="Wybrać plik", font=15,
                        command=lambda: self.load_the_data(file_label, initial_fs), bg="white")
        button.place(relx=0.4, rely=0.3, relwidth=0.1, relheight=0.4)
        file_label = Label(self.fileFrame, font=15, bg="#dfeff0", borderwidth=2, relief="ridge", anchor = 'e')
        file_label.place(relx=0.5, rely=0.3, relwidth=0.45, relheight=0.4)

    def check_the_fs(self, fs):
        if fs == "":
            m_box.showwarning('Uwaga', 'Najpierw wprowadż częstotliwość próbkowania sygnału')
            return False
        else:
            try:
                fs = int(fs)
            except ValueError:
                m_box.showerror('Błąd', 'Częstotliwośc próbkowania powinna być liczbą całkowitą')
                return False
            if fs <= 0 or fs > 100000:
                m_box.showerror('Błąd', 'Częstotliwość próbkowania powinna \nmieśić się w przedziale (0, 100000] Hz'
                                        '\n\n Wprowadż dane jeszcze raz!')
                return False
            else:
                return True


    def design_plot_frame(self):
        f = Figure(figsize=(5, 5), dpi=100)
        self.ax = f.add_subplot(111)
        self.plotFigure = FigureCanvasTkAgg(f, self.plotFrame)
        self.plotFigure.draw()
        self.plotFigure.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(self.plotFigure, self.plotFrame)
        toolbar.update()
        self.plotFigure._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def send_plot_frames(self):
        self.modificator.get_plot_frames(self.ax, self.plotFigure)

    def send_modified_data(self):
        scaling_rate = self.scalingRateEntry.get()
        t1 = self.lengthFrom.get()
        t2 = self.lengthTo.get()

        self.modificator.get_all_data(scaling_rate, t1, t2, self.nextButton)

    def load_the_data(self, fileLabel, initial_fs):
        self.fs = initial_fs.get()

        if self.check_the_fs(self.fs):
            if self.modificator.open_file(fileLabel, self.fs):
                self.modificator.overwrite(self.scalingRateEntry, self.lengthFrom, self.lengthTo)
                self.change_buttons_state()

    def change_buttons_state(self):
        self.applyButton.config(state='normal')
        self.nextButton.config(state='normal')

    def open_filtration_window(self):
        filtration_window = tk.Toplevel(self.window)
        filtration_window.geometry("1500x800")

        start_program(filtration_window, self.modificator.modified_data, self.fs)


class Modificator:
    def __init__(self):
        self.originalData = np.array([])
        self.scaling_rate = 1.
        self.t1 = 0
        self.t2 = len(self.originalData)
        self.fs = 0

    def open_file(self, file_label, fs):

        filename = filedialog.askopenfilename(title="Select a file",
                                              filetype=(("txt files", "*.txt"), ("tcv files", "*.tsv")))
        if filename == "":
            return False
        else:
            self.__init__()
            file_label["text"] = filename
            try:
                raw_data = loadtxt(filename)
                self.originalData = raw_data[:, 1]
                self.t2 = len(self.originalData)
                self.fs = int(fs)
            except Exception as e:
                m_box.showerror('Błąd odczytu pliku', str(e))
                return False
            return True

    def overwrite(self, scaling_rate_entry, t1_entry, t2_entry):
        scaling_rate_entry.config(state=NORMAL)
        scaling_rate_entry.delete(0, END)
        scaling_rate_entry.insert(0, self.scaling_rate)
        t1_entry.config(state=NORMAL)
        t1_entry.delete(0, END)
        t1_entry.insert(0, self.t1)
        t2_entry.config(state=NORMAL)
        t2_entry.delete(0, END)
        t2_entry.insert(0, self.t2/self.fs)

        self.modify_data()
        self.draw_plot()

    def modify_data(self):
        self.modified_data = self.originalData[self.t1:self.t2]
        self.modified_data = self.modified_data * self.scaling_rate
        self.draw_plot()

    def get_plot_frames(self, ax, plotFigure):
        self.ax = ax
        self.plotFigure = plotFigure

    def get_all_data(self, scaling_rate, t1, t2, nextButton):
        self.scaling_rate = scaling_rate
        self.t1 = t1
        self.t2 = t2

        if self.check_the_data_type() and self.check_the_correctness():
            nextButton.config(state="normal")
            self.modify_data()
        else:
            nextButton.config(state="disabled")

    def check_the_data_type(self):
        try:
            self.scaling_rate = float(self.scaling_rate)
        except ValueError:
            m_box.showerror('Błąd', 'Współczynnik skalowania powinien być liczbą')
        try:
            self.t1 = float(self.t1)
            self.t2 = float(self.t2)
        except ValueError:
            m_box.showerror('Błąd', 'Długość powinna być wyrażona liczbami w sekundach')
            return False
        return True

    def transform_data(self):
        self.t1 = int(self.t1 * self.fs)
        self.t2 = int(self.t2 * self.fs)

    def check_the_correctness(self):
        self.transform_data()
        error_text = ""

        if self.scaling_rate < -1000 or self.scaling_rate > 1000:
            error_text = error_text + "► Współczynnik skalowania powinien mieścić się \n     " \
                                      "w przedziale [-1000, 1000]\n"
        if self.t1 < 0 or self.t1 > (len(self.originalData) - 1):
            error_text = error_text + "► Wskazana wartość początku sygnału jest poza zakresem\n"
        if self.t2 == 0 or self.t2 > len(self.originalData) or self.t2 <= self.t1:
            error_text = error_text + "► Wskazana wartość końcu sygnału jest poza zakresem\n"
        if error_text == "":
            return True
        else:
            m_box.showerror('Błednie wprowadzone dane', f'{error_text}\nWprowadż dane jeszcze raz!')
            return False

    def draw_plot(self):

        times = arange(len(self.modified_data)) / self.fs + self.t1 / self.fs
        self.ax.clear()
        self.ax.set_title('Sygnał MKG', fontsize = 15)
        self.ax.set_xlabel('Czas [s]', fontsize = 10)
        self.ax.set_ylabel('Amplituda [pT]', fontsize = 10)

        self.ax.plot(times, self.modified_data)
        # self.ax.subtitle("kaka")
        self.plotFigure.draw()


def start_point():
    window = Tk()
    window.geometry("1500x800")

    modificator = Modificator()
    AppDesigner(modificator, window)

    window.mainloop()


start_point()
