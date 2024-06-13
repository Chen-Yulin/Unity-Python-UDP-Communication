# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

import UdpComms as U
import time

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

cat = "cat MIAO~"
pos = [0,0,0]
rot = [0,0,0]
size = [0.2,0.2,0.2]

direction = -1

def ObjectMsg(cat,px,py,pz,rx,ry,rz,sx,sy,sz):
    res = "{Object Detection}\n"
    res += cat + "\n"
    res += str(px) + "\n"
    res += str(py) + "\n"
    res += str(pz) + "\n"
    res += str(rx) + "\n"
    res += str(ry) + "\n"
    res += str(rz) + "\n"
    res += str(sx) + "\n"
    res += str(sy) + "\n"
    res += str(sz)
    return res

while True:
    sock.SendData(ObjectMsg(cat, pos[0], pos[1], pos[2], rot[0], rot[1], rot[2], size[0], size[1], size[2])) # Send this string to other application
    rot[1] += 1
    pos[0] += 0.02*direction

    if pos[0] > 1:
        direction = -1
    elif pos[0] < -1:
        direction = 1

    data = sock.ReadReceivedData() # read data

    if data != None: # if NEW data has been received since last ReadReceivedData function call
        print(data) # print new received data

    time.sleep(0.05)