#!/usr/bin/env python
"""
Client side: use sockets to send data to the server, and #print server's
reply to each message line; 'localhost' means that the server is running
on the same machine as the client, which lets us test client and server
on one machine;  to test over the Internet, run a server on a remote
machine, and set serverHost or argv[1] to machine's domain name or IP addr;
Python sockets are a portable BSD socket interface, with object methods
for the standard socket calls available in the system's C library;
"""

import sys
from socket import *              # portable socket interface plus constants
import datetime


serverHost = 'c58'          # server name, or: 'starship.python.net'
serverPort = 2007                # non-reserved port used by the server

message = [b'H'*1]*50000          # default text to send to server
                                            # requires bytes: b'' or str,encode()
if len(sys.argv) > 1:
    serverHost = sys.argv[1]                # server from cmd line arg 1
    if len(sys.argv) > 2:                   # text from cmd line args 2..n
        message = (x.encode() for x in sys.argv[2:])  

#sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
#sockobj.connect((serverHost, serverPort))   # connect to server machine + port

t1 = datetime.datetime.now()
for line in message:
    sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
    sockobj.connect((serverHost, serverPort))   # connect to server machine + port
    sockobj.setblocking(0)
    sockobj.send(line)                      # send line to server over socket
    leng=0
    data=''
    #print(len(line))
    while leng<len(line):
        try:
            tmp = sockobj.recv(1024)               # receive line from server: up to 1k
        except:continue
        leng += len(tmp)
        data += tmp
    #print(len(data))
    ##print('Client received:', data)         # bytes are quoted, was `x`, repr(x)
    sockobj.close()                             # close socket to send eof to server
t2 = datetime.datetime.now()
c=(t2-t1)
print(c.seconds,"s")
print(c.microseconds,"us")
