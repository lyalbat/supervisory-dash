import serial
import time
from datetime import datetime
import pytz
from tkinter import *
#from utils import variableUnitsByChar

ser = serial.Serial('COM4', baudrate = 9600, timeout=1)
time.sleep(.1)

def flushBuffer():
    ser.flushInput()
    ser.flushOutput()
    time.sleep(.1)

def changeValues(setpoint):
   command = "w" + "," + str(setpoint)
   ser.write(command.encode())
   data = ser.readline().decode().split('\r\n')[0]
   flushBuffer()
   print(data)
   return data

def submit():
    setpoint = entry.get()
    changeValues(setpoint)
def delete():
    entry.delete(0,END)

write_page = Tk()
write_page.geometry("420x420")
write_page.title("Sistema Supervisorio")
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
write_page.mainloop()