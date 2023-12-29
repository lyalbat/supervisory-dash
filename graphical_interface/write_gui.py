from tkinter import *
from tkinter import messagebox

def write_page():
    window = Tk()
    window.geometry("420x420")
    window.title("Pertubação do Sistema")
    window.config(background="black")

    def submit():
        setpoint = entry.get()
        print("Novo setpoint: " + str(setpoint))
    def delete():
        entry.delete(0,END)

    def returnToMenu():
        window.destroy()
        from main_gui import main
        main()
    def CloseWindow():
        if messagebox.askokcancel(title="Confirmacao",message="Deseja fechar o programa?"):
            window.destroy()

    menubar = Menu(window)
    window.config(menu=menubar)
    actionMenu = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Opções", menu=actionMenu)
    actionMenu.add_command(label="Menu Inicial",command=returnToMenu)
    actionMenu.add_command(label="Sair",command=CloseWindow) 

    writeText = "Escolha sua vazao desejada [m3/s]:\n"
    label = Label(
        window,
        text=writeText,
        font=('bold'),
        fg='white',
        bg='black',
        pady=20)
    label.pack()
    entry = Entry(window, font = ("Arial", 30))
    entry.pack()
    frame = Frame(window, bg="black", bd=1, width=400)
    frame.pack()
    submit_button = Button(frame, text="Enviar", command=submit).pack(side=RIGHT)
    delete_button = Button(frame, text="Deletar", command=delete).pack(side=LEFT)
    window.mainloop()