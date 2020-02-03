import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading
import serial

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)
    
def acq_window():    
    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()


def acq_serial():
    print('Serial acquisition is started')
    ser = serial.Serial('COM4', baudrate=9600, timeout=1)
    duration = 6000
    renew = 5
    TimeValue = 0

    f = open("sampleText.txt","w")
    f.close()

    f = open("sampleText.txt","a")

    for i in range(duration):
        s = ser.read(4)
        val = int.from_bytes(s, byteorder='big', signed=True)
        print(val)
        TimeValue = TimeValue + 1
        f.write(str(TimeValue))
        f.write(',')
        f.write(str(val))
        f.write('\n')
        if(i%renew == 0):
            f.close()
            f = open("sampleText.txt","a")
    
    ser.close()    

if __name__ == "__main__":
    back_task = threading.Thread(target = acq_serial)
    back_task.start()
    acq_window()
