from tkinter import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from utils import variableUnitsByChar
#from tkinter import messagebox

def plotting(sensor, sensor_label):
    print(f'{sensor} and {sensor_label}')
    '''plt.style.use('fivethirtyeight')
    def animate(i, sensor, sensor_label):
        data = pd.read_csv('sensor_history.csv')
        y = data[sensor]
        x = np.arange(len(y))
        plt.cla()
        plt.plot(x, y, label=sensor_label)
        plt.legend(loc='upper left')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate,frames=50,fargs=(sensor, sensor_label), interval=10)
    plt.tight_layout()
    plt.show()'''

def start_plot(sensor_var):
    config = variableUnitsByChar(sensor_var)
    plotting(config['name'], config['unit'])

def main():
    root = Tk()
    root.geometry("420x420")
    root.title("Sistema Supervisorio")
    root.config(background="black")

    def read():
        read_page = Toplevel()
        read_page.state("zoomed")
        read_page.config(background="black")

        def handleMenuRead(return_action):
            read_page.destroy()
            '''if(return_action == 'home'):
                read_page.destroy()
            else:
                read_page.destroy()'''

        menubar = Menu(read_page)
        read_page.config(menu=menubar)
        actionMenu = Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Opções", menu=actionMenu)
        actionMenu.add_command(label="Menu Inicial",command=lambda: handleMenuRead('home'))
        #actionMenu.add_command(label="Alterar Valor de SP", command=lambda: handleMenuRead('modify')) 
        
        fig,ax = plt.subplots()
        read_frame = Frame(read_page)
        label = Label(read_page, text="Plotting data", bg="black", fg="white")
        label.config(font=("Arial",25))
        label.pack()

        canvas = FigureCanvasTkAgg(fig, master=read_page)
        canvas.get_tk_widget().pack()
        read_frame.pack()
        sensor_var = StringVar(read_frame)
        OPTIONS  = ['v','c','t','f','h']
        sensor_var.set(OPTIONS[0]) # default value

        w = OptionMenu(read_frame, sensor_var, *OPTIONS)
        w.pack()
        Button(read_frame, text="Start Plotting", command=lambda: start_plot(sensor_var.get())).pack()
        
    def write():
        def submit():
            setpoint = entry.get()
            print("Novo setpoint: " + str(setpoint))
        def delete():
            entry.delete(0,END)
        write_page = Toplevel()
        write_page.state("zoomed")
        write_page.config(background="black")
        write_page.title("Pertubação do Sistema")
        writeText = "Escolha sua vazao desejada [m3/s]:\n"
        write_label = Label(
            write_page,
            text=writeText,
            font=('bold'),
            fg='white',
            bg='black',
            pady=20)
        write_label.pack()
        entry = Entry(write_page, font = ("Arial", 30))
        entry.pack()
        frame = Frame(write_page, bg="black", bd=1, width=400)
        frame.pack()
        submit_button = Button(frame, text="Enviar", command=submit).pack(side=RIGHT)
        delete_button = Button(frame, text="Deletar", command=delete).pack(side=LEFT)
        def handleMenuRead(return_action):
            write_page.destroy()
            '''if(return_action == 'home'):
                read_page.destroy()
            else:
                read_page.destroy()'''

        menubar = Menu(write_page)
        write_page.config(menu=menubar)
        actionMenu = Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Opções", menu=actionMenu)
        actionMenu.add_command(label="Menu Inicial",command=lambda: handleMenuRead('home'))
        
    photo = PhotoImage(file="image.png")
    image = Label(
        root,
        height=250,
        image=photo,
        compound=   "bottom")
    image.pack()

    labelText = "Bem vindo(a)." + "\n" + "Escolha uma ação: "
    label = Label(root, text=labelText,
        font=('Arial',15,'bold'),
        fg='white',
        bg='black',
        pady=20,
        bd=10)
    label.pack()

    activeColor = "#0679d3"

    frame = Frame(root, bg="black", bd=1, width=400)
    frame.pack()
    Button(frame,
        text="Monitorar sistema",
        command=read,
        font=('Arial',10),
        fg='black',
        bg='white',
        padx=10,
        activebackground=activeColor).pack(side="left")
    Button(frame,
        text="Alterar Set Point",
        command=write,
        font=('Arial',10),
        fg='black',
        bg='white',
        activebackground=activeColor).pack(side="right")

    root.mainloop()

main()