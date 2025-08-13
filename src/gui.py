import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
import time
import math
from matplotlib.animation import FuncAnimation

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
    

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-8, 8)
ax.set_ylim(-2, 8)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

# Draw Cartesian plane axes
ax.axhline(y=0, color='black', linewidth=1.5)
ax.axvline(x=0, color='black', linewidth=1.5)

# Add axis labels
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_title('Cartesian Plane with Semicircle and Rotating Line', fontsize=14)

# Draw semicircle (upper half only) with radius 5 centered at origin
theta_semicircle = np.linspace(0, np.pi, 100)
x_semicircle = 5 * np.cos(theta_semicircle)
y_semicircle = 5 * np.sin(theta_semicircle)
ax.plot(x_semicircle, y_semicircle, 'blue', linewidth=2, label='Semicircle (r=5)')

# Initialize the rotating line
line, = ax.plot([], [], 'red', linewidth=3, label='Rotating Line')
point, = ax.plot([], [], 'ro', markersize=8)

# Add legend
ax.legend()

def animate(frame):
    # Calculate angle for rotation (from -π to 0 for clockwise from left to right)
    # We use 180 frames to complete the semicircle rotation
    angle = np.pi - (frame * np.pi / 180)  # Start from π (left) to 0 (right)
    
    # Calculate end point of the line (length 5)
    x_end = 5 * np.cos(angle)
    y_end = 5 * np.sin(angle)
    
    # Update line coordinates (from origin to end point)
    line.set_data([0, x_end], [0, y_end])
    
    # Update point at the end of the line
    point.set_data([x_end], [y_end])
    
    return line, point

# Create animation
# 181 frames to include both start and end positions
anim = FuncAnimation(fig, animate, frames=181, interval=50, blit=True, repeat=True)

# Show the plot
plt.tight_layout()
plt.show()
