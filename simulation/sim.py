#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import _thread
import time
import datetime

host = '0.0.0.0'
port = 1234
buf = 1024

addr = (host, port)

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind(addr)
serversocket.listen(10)

clients = [serversocket]

def handler(clientsocket, clientaddr):
    print("Accepted connection from: ", clientaddr)
    while True:
        data = clientsocket.recv(1024)
        print(data.decode('utf-8'))
        if data.decode('utf-8') == "bye\n" or not data:
            break

        elif data.decode('utf-8') == "test1\n":
            clientsocket.send("test1\n".encode())

        else:
            clientsocket.send(("ECHO: " + data.decode('utf-8') + '\n').encode())

    #clients.remove(clientsocket)
    #clientsocket.close()

def push():
    while True:      
        for i in clients:
            if i is not serversocket: # neposilat sam sobe
                i.send(("Curent date and time: " + str(datetime.datetime.now()) + '\n').encode())
        time.sleep(1) # [s]


_thread.start_new_thread(push, ())

while True:
    try:
        print("Server is listening for connections\n")
        clientsocket, clientaddr = serversocket.accept()
        clients.append(clientsocket)
        _thread.start_new_thread(handler, (clientsocket, clientaddr))
    except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
        print("Closing server socket...")
        serversocket.close()
        break