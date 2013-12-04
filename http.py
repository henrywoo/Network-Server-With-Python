#!/usr/local/python3/bin/python3
# -*- coding: utf-8 -*-

import socket, select
import signal
import sys

def handleINT(signum,frame):
  """SIGINT handler"""
  print("signum:%d,frame:%s" % (signum,frame))
  print( "---- good bye ----")
  sys.exit(0)

def int2byte(i):
  return str(i).encode('utf-8')

signal.signal(signal.SIGINT,handleINT)

port=8080

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
content = b'Hello, world!'
response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: ' + int2byte(len(content)) + b'\r\n\r\n'
response += content

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#address reusable + disable nagle
serversocket.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, 1)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serversocket.bind(('0.0.0.0', port))
serversocket.listen(1)

#nonblocking IO
serversocket.setblocking(0)

#linux epoll
epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
   connections = {}; requests = {}; responses = {}
   while True:
      events = epoll.poll(1) #block here - epoll_wait?
      for fileno, event in events:
         print(fileno,event)
         if fileno == serversocket.fileno():
            connection, address = serversocket.accept()
            print("connection:%s address:%s" % (connection, address))
            connection.setblocking(0)
            print("connection.fileno:%d" % (connection.fileno()))
            epoll.register(connection.fileno(), select.EPOLLIN)
            connections[connection.fileno()] = connection
            requests[connection.fileno()] = b''
            responses[connection.fileno()] = response
         elif event & select.EPOLLIN:
            requests[fileno] += connections[fileno].recv(1024)
            if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
               epoll.modify(fileno, select.EPOLLOUT)
               print('-'*40 + '\n' + requests[fileno].decode()[:-2])
         elif event & select.EPOLLOUT:
            byteswritten = connections[fileno].send(responses[fileno])
            responses[fileno] = responses[fileno][byteswritten:]
            if len(responses[fileno]) == 0:
               epoll.modify(fileno, 0)
               connections[fileno].shutdown(socket.SHUT_RDWR)
         elif event & select.EPOLLHUP:
            epoll.unregister(fileno)
            connections[fileno].close()
            del connections[fileno]
finally:
   epoll.unregister(serversocket.fileno())
   epoll.close()
   serversocket.close()
