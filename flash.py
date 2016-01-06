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
    time.sleep(2)
except:
    print "Open port %s error" % port
    sys.exit(1)


print "Ok, now download init.lua script..."
lines = 0
try:
    lines = open("init.lua", "r").readlines()
except:
    print "Open init.lua error, please put init.lua in current directory"
    sys.exit(1)

nodewrite('file.remove("init.lua")\r\n')
nodewrite('file.open("init.lua", "w+")\r\n')

for line in lines:
    if line.endswith('\n'):
        line = line[:-1]
    cmd = "file.writeline(%s)\r\n" % repr(line)
    print cmd[:-2]
    nodewrite(cmd)
    
nodewrite('file.close()\r\n')
print "\nDone"
s.close()
