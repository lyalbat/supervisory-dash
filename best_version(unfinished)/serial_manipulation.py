import serial
import time
from datetime import datetime
import pytz
import csv
ser = serial.Serial('COM3', baudrate = 9600, timeout=1)
time.sleep(.1)

fieldnames = ["full_date","timestamp","voltage","current","temperature","flow_rate","hydrogen"]

def writeToFile(full_date,timestamp,voltage,current,temperature,flow_rate,hydrogen):
    with open('sensor_history.csv','a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            info = {
                "full_date": full_date,
                "timestamp": timestamp,
                "voltage": voltage,
                "current": current,
                "temperature": temperature,
                "flow_rate": flow_rate,
                "hydrogen": hydrogen
            }
            csv_writer.writerow(info)
    time.sleep(5)

def formatBeforeWrite(res):
    now = datetime.now(tz = pytz.timezone('America/Recife'))
    full_date = now.strftime('%d/%m/%Y')
    timestamp = now.strftime('%H:%M:%S')
    if(len(res)> 1):
        writeToFile(full_date,timestamp,voltage=res[0],current=res[1],temperature=res[2],flow_rate=res[3],hydrogen=res[4])
    else:
        pass

def flushBuffer():
    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)

def getValues():
    ser.write("r,-1".encode())
    data = ser.readline().decode().split('\r\n')[0]
    treatedData = data.split(",")
    print(treatedData)
    flushBuffer()
    print(treatedData)
    return treatedData


def changeValues(setpoint):
   command = "w" + "," + str(setpoint)
   ser.write(command.encode())
   data = ser.readline().decode().split('\r\n')[0]
   print("from serial read:")
   print(data)
   flushBuffer()
   return data

def main_serial():
    closeProgram=False
    keepReading=True
    keepWriting=False
    setpoint=-1

    if(keepReading):
        while keepReading:
            data = getValues()
            formatBeforeWrite(data)
    if(keepWriting):
        if(setpoint != -1):
            changeValues(setpoint)
            return 1
        return 0

main_serial()