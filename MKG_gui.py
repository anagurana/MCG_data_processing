from tkinter import *
from tkinter import filedialog

from scipy import *

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

# from MKG_GUI_Filtering import create_filtration_window
from MKG_app import start_program

originalData = []
Fs = 0
scaling_rate = 1.0
t1 = 0
t2 = 0

def open_file():
    global originalData
    global Fs
    global scaling_rate
    global t1
    global t2

    Fs = 1000
    scaling_rate = 1.0
    t1 = 0

    filename = filedialog.askopenfilename(title="Select a file",
                                          filetype=(("txt files", "*.txt"), ("tcv files", "*.tsv")))
    fileLabel["text"] = filename
    rawdata = loadtxt(filename)
    originalData = rawdata[:, 1]

    t2 = len(originalData)
    overwrite()
    modified_data = modify_data()
    draw_modified_data(modified_data)


def overwrite():
    samplingRate.delete(0, END)
    samplingRate.insert(0, Fs)
    scalingRate.delete(0, END)
    scalingRate.insert(0, scaling_rate)
    lengthFrom.delete(0, END)
    lengthFrom.insert(0, t1)
    lengthTo.delete(0, END)
    lengthTo.insert(0, t2/Fs)


def open_new_window():
    data = modify_data()
    # create_filtration_window(data)
    start_program(data)


def modify_data():
    data = originalData[t1:t2]
    data = data * scaling_rate
    return data


def draw_modified_data(data):
    times = arange(len(data)) / Fs + t1/Fs

    drawn_plot.clear()
    drawn_plot.plot(times, data)
    plotFigure.draw()


def modify_plot():
    global Fs
    global scaling_rate
    global t1
    global t2

    Fs = int(samplingRate.get())
    scaling_rate = float(scalingRate.get())
    t1 = int(float(lengthFrom.get())*Fs)
    t2 = int(float(lengthTo.get())*Fs)
    modified_data = modify_data()
    draw_modified_data(modified_data)


top = Tk()
top.geometry("1500x800")

fileF = Frame(top)
fileF.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.1)
plotF = Frame(top)
plotF.place(relx=0.01, rely=0.11, relwidth=0.98, relheight=0.7)
modF = Frame(top, bg='#3c9162', bd=4)
modF.place(relx=0.01, rely=0.81, relwidth=0.98, relheight=0.18)


button = Button(fileF, text="Wybrać plik", bg='#f5ce93', font=15, command=open_file)
button.pack(side='left', fill='both')
fileLabel = Label(fileF, font=15)
fileLabel.pack(side='left', fill='both', expand=True)


f = Figure (figsize=(5,5), dpi=100)
drawn_plot = f.add_subplot(111)
plotFigure = FigureCanvasTkAgg(f, plotF)
plotFigure.draw()
plotFigure.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
toolbar = NavigationToolbar2Tk(plotFigure, plotF)
toolbar.update()
plotFigure._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)


fsLabel = Label(modF, text="Częstotliwość próbkowania", font=15)
fsLabel.place(relx=0, rely=0.2, relwidth=0.2, relheight=0.2)
samplingRate = Entry(modF, font=15, justify=CENTER)
samplingRate.place(relx=0.2, rely=0.2, relwidth=0.21, relheight=0.2)

scalingL = Label(modF, text="Współczynnik skalowania", font=15)
scalingL.place(relx=0, rely=0.4, relwidth=0.2, relheight=0.2)
scalingRate = Entry(modF, font=15, justify=CENTER)
scalingRate.place(relx=0.2, rely=0.4, relwidth=0.21, relheight=0.2)

lengthL = Label(modF, text="Długość: [s]", font=15)
lengthL.place(relx=0, rely=0.6, relwidth=0.2, relheight=0.2)
lengthFrom = Entry(modF, font=15, justify=CENTER)
lengthFrom.place(relx=0.2, rely=0.6, relwidth=0.1, relheight=0.2)

lengthLabel = Label(modF, text=" : ", font=15)
lengthLabel.place(relx=0.3, rely=0.6, relwidth=0.01, relheight=0.2)
lengthTo = Entry(modF, font=15, justify=CENTER)
lengthTo.place(relx=0.31, rely=0.6, relwidth=0.1, relheight=0.2)

applyB = Button(modF, text="Zastosuj", font=15, command= modify_plot)
applyB.place(relx=0.5, rely=0.2, relwidth=0.2, relheight=0.6)
nextB = Button(modF, text="Przejdź do filtracji", font=15, command = open_new_window)
nextB.place(relx=0.75, rely=0.2, relwidth=0.2, relheight=0.6)


top.mainloop()
