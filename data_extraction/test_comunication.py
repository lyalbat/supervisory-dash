import serial
import time

print("working ok")

ser = serial.Serial('COM4', baudrate = 9600, timeout=1)
time.sleep(3)
numPoints = 4
dataList = [0]*numPoints

def getValues():
    ser.write("r,-1".encode())
    for i in range(0, numPoints):
        dataList[i] = ser.readline().decode().split('\r\n')[0]
    return dataList

def changeValues(setpoint):
   command = "w" + "," + str(setpoint)
   ser.write(command.encode())

while(1):
    userInput = input('Would you like to monitor the system [m] or change set point [c] ? ')
    if userInput == 'm':
        data = getValues()
        print(data)
    elif userInput == 'c':
        setpoint = input('What is your desired setpoint [use point notation. eg: 1.0] ? ')
        changeValues(setpoint)
