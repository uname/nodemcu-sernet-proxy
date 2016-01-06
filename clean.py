#-*- coding: utf-8 -*-
import serial
import sys
import time

s = 0
nodewrite = lambda data: s.write(data) and time.sleep(0.2)

port = raw_input("Input com port: ")
if len(port) < 4 or port[:3].lower() != "com" or not port[3:].isdigit():
    sys.exit(1)

try:
    print "Port is opening, please waite..."
    s = serial.Serial(port, 9600)
    time.sleep(3)
except:
    print "Open port %s error" % port
    sys.exit(1)
    
print "Ok, now clean init.lua"
nodewrite('--quitproxy\r\n')
nodewrite('file.remove("init.lua")\r\n')
print "\nDone"
s.close()
