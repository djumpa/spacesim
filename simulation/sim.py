#!/usr/bin/env python3

import socket
import threading
import time
import datetime


host = '0.0.0.0'
port = 1234
buf = 1024

addr = (host, port)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    try:
        while True: 
            velocity = [0.0, 0.0, 0.0]
            position = [0.0, 1.0, 2.0]

            velocity_str = "VEL:"+str(velocity[0]) + " " +  str(velocity[1]) + " " + str(velocity[2])    
            position_str = "POS:"+str(position[0]) + " " +  str(position[1]) + " " + str(position[2])    

            for i in clients:
                if i is not serversocket: # neposilat sam sobe
                    i.send((velocity_str+'\n'+position_str+'\n').encode())
            time.sleep(0.1) # [s]
    except ConnectionResetError:
        print("Connection ended on the otherside")
        exit

x = threading.Thread(target=push, args=())
x.start()

while True:
    try:
        print("Server is listening for connections")

        clientsocket, clientaddr = serversocket.accept()
        clients.append(clientsocket)

        #y = threading.Thread(target=handler, args=(clientsocket, clientaddr))
        #y.start()

    except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
        print("Closing server socket...")
        serversocket.close()
        break
