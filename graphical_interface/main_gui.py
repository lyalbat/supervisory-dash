from tkinter import *
from write_gui import write_page

def main():
    window = Tk()
    window.geometry("420x420")
    window.title("Sistema Supervisorio")
    window.config(background="black")

    def read():
        from read_gui import read_page
        window.destroy()
        read_page()
    def write():
        window.destroy()
        write_page()

    photo = PhotoImage(file="image.png")
    image = Label(
        window,
        height=250,
        image=photo,
        compound=   "bottom")
    image.pack()

    labelText = "Bem vindo." + "\n" + "Escolha uma ação: "
    label = Label(window, text=labelText,
        font=('bold'),
        fg='white',
        bg='black',
        pady=20,
        bd=10)
    label.pack()

    activeColor = "#0679d3"

    frame = Frame(window, bg="black", bd=1, width=400)
    frame.pack()
    Button(frame,
        text="Monitorar sistema",
        command=read,
        font=('bold'),
        fg='black',
        bg='white',
        padx=10,
        activebackground=activeColor).pack(side="left")
    Button(frame,
        text="Alterar Set Point",
        command=write,
        font=('bold'),
        fg='black',
        bg='white',
        activebackground=activeColor).pack(side="right")

    window.mainloop()

main()