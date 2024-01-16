import serial
import time
from datetime import datetime
import pytz
import csv
ser = serial.Serial('COM3', baudrate = 9600, timeout=1)
time.sleep(.1)

fieldnames = ["full_date","timestamp","voltage","current","temperature","flow_rate","hydrogen","pulse_count"]
path = r'C:\Users\SUPERVISORIO\Documents\supervisory-system\minimal_version\read\sensor_history.csv'

def writeToFile(full_date,timestamp,voltage,current,temperature,flow_rate,hydrogen,pulse):
    with open(path,'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            info = {
                "full_date": full_date,
                "timestamp": timestamp,
                "voltage": voltage,
                "current": current,
                "temperature": temperature,
                "flow_rate": flow_rate,
                "hydrogen": hydrogen,
                "pulse_count": pulse,
            }
            csv_writer.writerow(info)
    time.sleep(5)

def formatBeforeWrite(res):
    now = datetime.now(tz = pytz.timezone('America/Recife'))
    full_date = now.strftime('%d/%m/%Y')
    timestamp = now.strftime('%H:%M:%S')
    if(len(res)> 1):
        if(res[3] != -1):
            writeToFile(full_date,timestamp,voltage=res[0],current=res[1],temperature=res[2],flow_rate=res[3],hydrogen=res[4],pulse=res[5])
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

def main_serial():
    while True:
        data = getValues()
        formatBeforeWrite(data)

main_serial()