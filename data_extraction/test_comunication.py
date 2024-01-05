import serial
import time
from datetime import datetime
import pytz

ser = serial.Serial('COM4', baudrate = 9600, timeout=1)
time.sleep(.1)
numPoints = 5
dataList = [0]*numPoints
#v - voltage / c - current / t - temperature / f - flow rate / h - hydrogen concentration
sensors = ['v','c','t','f','h']

def formatValuesByOrder(res):
    now = datetime.now(tz = pytz.timezone('America/Recife'))
    current_time = now.strftime("%H:%M")
    day = now.strftime('%d-%m-%Y')
    formattedDate = "Data: " + day + "\nHora: " + current_time + "\n"
    formattedEnergyResponse = "Tensao: " + str(res[0]) + "V \nCorrente:" +  str(res[1]) + "A\n"
    formattedPhysicalResponse = "Temperatura: " +  str(res[2]) + "°C \nVazao: " +  str(res[3]) + "l/m\n"
    formattedChemicalResponse =  "Hidrogenio: " +  str(res[4]) + "ppm"
    return formattedDate + formattedEnergyResponse + formattedPhysicalResponse + formattedChemicalResponse

def flushBuffer():
    ser.flushInput()
    ser.flushOutput()
    time.sleep(.1)

def getValues():
    ser.write("r,-1".encode())
    data = ser.readline().decode().split('\r\n')[0]
    treatedData = data.split(",")
    flushBuffer()
    return treatedData

def changeValues(setpoint):
   command = "w" + "," + str(setpoint)
   ser.write(command.encode())
   data = ser.readline().decode().split('\r\n')[0]
   flushBuffer()
   print(data)
   return data

while(1):
    userInput = input('Would you like to monitor the system [m] or change set point [c] ? ')
    if userInput == 'm':
        try:
            data = getValues()
            print(formatValuesByOrder(data))
        except:
            print("Error: could not get sensor values")       
    elif userInput == 'c':
        setpoint = input('What is your desired setpoint [use point notation. eg: 1.0] ? ')
        print(changeValues(setpoint))
        """if(changeValues(setpoint)):
            print("You sucessfully set the new set point!")
        else:
            print("Error: could not input new setpoint")    """
