#!/usr/bin/env python
import socket
import select, time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool, Process
from Queue import Queue
import os

p = Pool(50)
def f(x):
    return x*x
isblocking = 0
queuedconnections = 5
server_socket = None
ep=None
q = Queue()
q2 = Queue()


def handle_input(socket, data):
    print("got data:",data)
    #todo
    socket.send(data) # sendall() partial?

def handle_request(fileno):
    if event & select.POLLIN:# to be removed
        #client_socket = connections[fileno]
        client_socket = q2.get()
        data = client_socket.recv(4096);
        #todo
        #time.sleep(5)
        if data:
            handle_input(client_socket, data)
        else:
            ep.unregister(fileno)
            client_socket.close()
            #del connections[fileno]
            #del handlers[fileno]

def handle_accept(ep_):
    (client_socket, client_address) = server_socket.accept()
    print "got connection from", client_address
    client_socket.setblocking(isblocking)
    ep_.register(client_socket.fileno(), select.POLLIN)
    q2.put(client_socket)

if __name__=='__main__2':
    #p.map(f, [1,2,3])
    pass

def worker():
    while True:
        fileno = q.get()
        handle_request(fileno)
        q.task_done()


if __name__=='__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 2007))
    server_socket.listen(queuedconnections)
    server_socket.setblocking(isblocking)

    #should start multiprocess here!!!
    pid=os.fork()
    if(pid==0):#child
        SpawnIOProcess(server_socket)
    else:
        while True:
            time.sleep(10)
    ep = select.epoll()
    ep.register(server_socket.fileno(), select.POLLIN|select.EPOLLET)
    print (server_socket.fileno())
    #handlers[server_socket.fileno()] = handle_accept #socket fd -> functor

    #pl = Pool(processes=10)
    p = Process(target=worker,args=())

    #proc 1: epoll
    sn=server_socket.fileno()
    while True:
        events = ep.poll()  # 10 seconds
        print(events)
        for fileno, event in events:
            if(fileno==sn):
                handle_accept(ep)
            else:
                print(fileno, event)
                q.put(fileno)
                if not p.is_alive():
                    p.start()
                #result = pl.apply_async(worker, [])


            ##handlers[fileno](fileno,event)
            # put into the Queue
