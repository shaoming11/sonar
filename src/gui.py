import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
import time
from tkinter import *
from tkinter import ttk

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
    
root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()