import tkinter as tk
from tkinter import Menu, Frame
from tkinter import messagebox

def read_page():
    def returnToMenu():
        window.destroy()
        from main_gui import main
        main()

    def CloseWindow():
        if messagebox.askokcancel(title="Confirmacao",message="Deseja fechar o programa?"):
            window.destroy()
    def HandleButton(char,name,unit, limits):
        window.destroy()
        #essa lista [LIMITS] é referente aos valores possiveis da variavel (min, max)
        from sensor_plot import readSensorData
        readSensorData(char,name,unit,limits)
    
    window = tk.Tk()
    window.config(background="black")
    window.title('Monitoring Dash')
    window.geometry('700x500')

    #widgets 
    main_title = tk.Label(
        window,
        text = 'Terminal do Sistema Primário',
        pady=40,
        fg='white',
        bg='black',
        font=('Arial',20,'bold'))
    sub_title = tk.Label(
        window,
        text='Clique no botão referente à variável de interesse',
        font =('Arial',10,'bold'),
        fg='white',
        bg='black')
    main_title.pack()
    sub_title.pack()

    big_frame = Frame(window, bg="black", bd=1, width=700, pady=50)
    big_frame.pack()

    top_frame = Frame(big_frame, bg="black", bd=1, width=700,height=500, pady=5)
    top_frame.pack()
    top_frame.columnconfigure((0,1,2), weight=1,uniform='a')

    bottom_frame = Frame(big_frame, bg="black", bd=1, width=700,height=500, pady=5)
    bottom_frame.pack()
    bottom_frame.columnconfigure((0,1), weight=1,uniform='a')
    
    hydrogen_btn = tk.Button(top_frame,
            text='Hidrogenio [ppm]',
            command=HandleButton('h','Concentracao de Hidrogenio','ppm',[0,2]))
    voltage_btn = tk.Button(top_frame,
             text='Tensao [V]',
             command=HandleButton('v','Tensao','V',[3,5]))
    current_btn = tk.Button(top_frame,
            text='Corrente [A]',
            command=HandleButton('c','Corrente','A',[4,6]))
    temperature_btn = tk.Button(bottom_frame,
            text='Temperatura [°C]',
            command=HandleButton('t','Temperatura','°C',[10,50])) 
    flow_rate_btn = tk.Button(bottom_frame,
            text='Vazao [l/min]',
            command=HandleButton('f','Vazao','l/min',[1,3]))
    
    temperature_btn.grid(row=0,column=0, sticky='wnse',ipadx=30)
    flow_rate_btn.grid(row=0,column=1, sticky='wnse',ipadx=25)
    hydrogen_btn.grid(row=1,column=0, sticky='wnse')
    voltage_btn.grid(row=1,column=1, sticky='wnse')
    current_btn.grid(row=1,column=2, sticky='wnse')

    menubar = Menu(window)
    window.config(menu=menubar)
    actionMenu = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Opções", menu=actionMenu)
    actionMenu.add_command(label="Menu Inicial",command=returnToMenu)
    actionMenu.add_command(label="Sair",command=CloseWindow)
    window.mainloop()
