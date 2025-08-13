import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
import time
import math

ser = 5 # serial.Serial(port='/dev/cu.usbmodem1101', baudrate=9600, timeout=1)

def findPort():
    ports = serial.tools.list_ports.comports()
    portsList = []
    for port in ports:
        print(str(port))
        portsList.append(str(port))
    
    val = input("Input: ")
    portSelected = val
    return portSelected

"""
tasks
- create gui
- load 180 degree semicircle
- every frame or so show a highlighted green line thats like a tracker
- when ultrasonic detects distance < X amount, highlight that line red permanently (based on pos)

matplotlib.animation
draw semi circle with lines around

step 1 get the serial print working
step 2 draw semicircle and lines
step 3 animate a line going aroudn the semi circle
step 4 handle logic for ultrasound detection (distance < X, change colour of point)
"""

def getInput():
    ser.write(b'g')
    time.sleep(0.1)
    return ser.readline().decode('ascii')

def main():
    time.sleep(3)
    ser.close()
    ser.open()
    
    while True:
        userInput = input("?")
        if userInput == 'g':
            print(getInput())
        # if ser.in_waiting:
        #     packet = ser.readline()
        #     if packet != b'\xff':
        #         print(packet.decode('utf', errors='ignore'))
    
# GRAPHING + ANIMATIONS
xmin, xmax, ymin, ymax = -5, 5, -5, 5
ticks_frequency = 1

fig, ax = plt.subplots(figsize=(10,10))
fig.patch.set_facecolor('#ffffff')

ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_xlabel('$x$', size=14, labelpad=-24, x=1.02)
ax.set_ylabel('$y$', size=14, labelpad=21, y=1.02, rotation=0)

plt.text(0.49, 0.49, r"$0$", ha='right', va='top', transform=ax.transAxes, horizontalalignment='center', fontsize=14)

x_ticks = np.arange(xmin, xmax+1, ticks_frequency)
y_ticks = np.arange(ymin, ymax+1, ticks_frequency)
ax.set_xticks(x_ticks[x_ticks != 0])
ax.set_yticks(y_ticks[y_ticks != 0])
ax.set_xticks(np.arange(xmin, xmax+1), minor=True)
ax.set_yticks(np.arange(ymin, ymax+1), minor=True)

ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

def func(x):
    return ((x - 1 ) ** 2) - 2

def semicircle(x, r):
    """
    x2 + y = r2
    r2-x2
    
    """
    l = []
    for i in x:
        l.append(math.sqrt(pow(r, 2) - pow(i, 2)))
    return l # 
 
x = np.linspace(-5, 5, 100)
y = semicircle(x, 5)
 
plt.plot(x, y, 'b', linewidth=2)
print([x, semicircle(x, 5)])
plt.show()