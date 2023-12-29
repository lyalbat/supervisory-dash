from tkinter import *
from tkinter import messagebox

def read_page():
    def returnToMenu():
        window.destroy()
        from main_gui import main
        main()
    def CloseWindow():
        if messagebox.askokcancel(title="Confirmacao",message="Deseja fechar o programa?"):
            window.destroy()
        
    window = Tk()
    window.title("Monitoramento do Sistema")
    window.config(background="black")

    menubar = Menu(window)
    window.config(menu=menubar)
    actionMenu = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Opções", menu=actionMenu)
    actionMenu.add_command(label="Menu Inicial",command=returnToMenu)
    actionMenu.add_command(label="Sair",command=CloseWindow)
    writeText = "UAU VARIOS GRAFICOS!! MUITO LEGAL:\n"
    label = Label(
        window,
        text=writeText,
        font=('bold'),
        fg='white',
        bg='black',
        pady=20)
    label.pack()
    print("You want to read a value")
    window.mainloop()
