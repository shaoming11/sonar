import serial.tools.list_ports

def findPort():
    ports = serial.tools.list_ports.comports()
    portsList = []
    for port in ports:
        portsList.append(str(port))
    print(portsList)
    
    val = input("Input: COM")
    portSelected = "COM" + str(val)
    return portSelected

"""
tasks
- create gui
- load 180 degree semicircle
- every frame or so show a highlighted green line thats like a tracker
- when ultrasonic detects distance < X amount, highlight that line red permanently (based on pos)
"""

def main():
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = findPort()
    serialInst.open()
    
    while True:
        if (serialInst.in_waiting):
            packet = serialInst.readline()
            print(packet.decode('utf'))
    
main()