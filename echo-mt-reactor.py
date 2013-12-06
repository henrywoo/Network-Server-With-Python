#!/usr/bin/env python
import socket
import select, time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool, Process
from Queue import Queue
import os,sys

isblocking = 0
queuedconnections = 5
server_socket = None

def handle_input(socket, data):
    try:
        #print("got data:",data)
        count=0
        sz=len(data)
        while (count<sz):
            sent = socket.send(data) # sendall() partial???
            #print("sent out %d bytes\n" % sent)
            count += sent
            if sent == 0:
                raise RuntimeError("socket connection broken")

    except Exception as e:
        print "pid=",os.getpid(),",error({0}): {1}".format(e.errno, e.strerror), ", Unexpected error:", sys.exc_info()[0]
        pass

def SpawnIOProcess(ss):
    """ss - server socket"""
    #time.sleep(2)
    ep = select.epoll()
    ssno = ss.fileno()
    ep.register(ssno, select.POLLIN|select.EPOLLET) # edge trigger more effective
    print("register ",ssno," into interest list of pid=",os.getpid())
    connections = {}

    while True:
        events = ep.poll()  # infinitely waiting
        for fileno, event in events:
            if fileno==ssno:
                try:
                    (client_socket, client_address) = ss.accept()
                    #print("pid:",os.getpid())
                    lno = client_socket.fileno()
                    #print "got connection from", client_address
                    client_socket.setblocking(isblocking)
                    ep.register(lno, select.POLLIN|select.EPOLLET)
                    #print("register ",lno," into interest list of pid=",os.getpid())
                    connections[lno] = client_socket
                except Exception as e:
                    #print "pid=",os.getpid(),",error({0}): {1}".format(e.errno, e.strerror), ", Unexpected error:", sys.exc_info()[0]
                    pass
            else:
                if event & select.POLLIN:
                    client_socket = connections[fileno]
                    try:
                        tmp=client_socket.recv(1024)
                        data=''
                        while tmp:
                            data += tmp
                            #print len(data)
                            tmp=client_socket.recv(1024)#,select.MSG_DONTWAIT)####??
                    except Exception as e:pass
                        #print "pid=",os.getpid(),",error({0}): {1}".format(e.errno, e.strerror), ", Unexpected error:", sys.exc_info()[0]
                if data:
                    handle_input(client_socket, data)####
                else:
                    ep.unregister(fileno)####
                    #print("unregister ",fileno," into interest list of pid=",os.getpid())
                    client_socket.close()
                    del connections[fileno]
                    #time.sleep(60)

if __name__=='__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 2007))
    server_socket.listen(queuedconnections)
    server_socket.setblocking(isblocking)

    #should start multiprocess here!!!
    ps=[]
    for i in xrange(10):# num of process 5
        ps.append(Process(target=SpawnIOProcess, args=(server_socket,)))

    for p in ps:
        p.start()
    for p in ps:
        p.join()
