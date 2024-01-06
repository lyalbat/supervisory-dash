import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def readSensorData(variable_char,variable_name,variable_unit, common_values):
    def animate(i, dataList, ser):
        command = variable_char + ',' + '-1'
        ser.write(command.encode())                                
        arduinoData_string = ser.readline().decode('ascii') 
        try:
            arduinoData_float = float(arduinoData_string)  
            dataList.append(arduinoData_float)             
        except:                                                                            
            pass
        dataList = dataList[-50:]                           
        ax.clear()                                          
        ax.plot(dataList)
        ax.set_ylim(common_values)                         
        ax.set_title(variable_name)                        
        ax.set_ylabel(variable_unit)                               

    dataList = []                                                                                                
    fig = plt.figure()                                     
    ax = fig.add_subplot(111)                               

    ser = serial.Serial("COM4", 9600)                       
    time.sleep(2)                                           

    ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(dataList, ser), interval=100) 
    plt.show()                                              
    ser.close()                                            

readSensorData('t','Temperatura','°C',[20,70])