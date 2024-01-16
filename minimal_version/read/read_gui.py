from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from utils import variableUnitsByChar

def plotting(sensor, sensor_label):
    plt.style.use('fivethirtyeight')
    def animate(i, sensor, sensor_label):
        path = r'C:\Users\SUPERVISORIO\Documents\supervisory-system\minimal_version\read\sensor_history.csv'
        data = pd.read_csv(path)
        y = data[sensor]
        x = np.arange(len(y))
        plt.cla()
        plt.plot(x, y, label=sensor_label)
        plt.legend(loc='upper left')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate,frames=50,fargs=(sensor, sensor_label), interval=10)
    plt.tight_layout()
    plt.show()

def start_plot(sensor_var):
    config = variableUnitsByChar(sensor_var)
    plotting(config['name'], config['unit'])

def read_page():
    read_page = Tk()
    read_page.state("zoomed")
    read_page.title("Sistema Supervisorio")
    read_page.config(background="black")

    fig,ax = plt.subplots()
    read_frame = Frame(read_page)
    label = Label(read_page, text="Plotting data", bg="black", fg="white")
    label.config(font=("Arial",25))
    label.pack()

    canvas = FigureCanvasTkAgg(fig, master=read_page)
    canvas.get_tk_widget().pack()
    read_frame.pack()
    sensor_var = StringVar(read_frame)
    OPTIONS  = ['tensao','corrente','temperatura','vazao','concentracao','pulsos']
    sensor_var.set(OPTIONS[0]) # default value

    w = OptionMenu(read_frame, sensor_var, *OPTIONS)
    w.pack()
    Button(read_frame, text="Start Plotting", command=lambda: start_plot(sensor_var.get())).pack()
    
    read_page.mainloop()

read_page()