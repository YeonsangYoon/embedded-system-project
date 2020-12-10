#!/usr/bin/python3
import os, sys
import time
import serial

port = '/dev/ttyUSB0' 
ser = serial.Serial(port, 38400, timeout = 2)
time.sleep(1)
count = 0
for _ in range(1):
    ser.write('3'.encode())
    #ser.write(b'3')
    #time.sleep(3)
    #ser.write(b'2')
    while(ser.readable()):
        ret = ser.readline()
        print(ret.decode(), type(ret.decode()), type(ret), ret)
        """
        if ret.decode() == 'a':
            break
        elif count > 5:
            #print('ERROR')
            break
        else:
            count += 1
        """

ser.close()

"""
time.sleep(10)

ser.write('2'.encode())
while(ser.readable()):
    ret = ser.read()
    print(ret.decode())
#ser.write('3'.encode())
#ser.write('4'.encode())
"""