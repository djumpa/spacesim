#!/usr/bin/env python3

import socket
import threading
import time
import datetime
import numpy as np
import json


host = '0.0.0.0'
port = 1234
buf = 1024

addr = (host, port)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(addr)
serversocket.listen(10)

clients = [serversocket]

bodies = []

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
            for i in clients:
                if i is not serversocket: # neposilat sam sobe
                    i.send(json.dumps(bodies).encode())
            time.sleep(0.1) # [s]
    except ConnectionResetError:
        print("Connection ended on the otherside")
        exit

def sim_loop():
    print("Start of sim thread")
    # Inital conditions and constants
    G = 1
    dt = 0.1

    sc = {
        "pos" : [101.0, 0.0, 0,0],
        "vel" : [0.0, 0.0, 0,0],
        "mass": 10
    }

    sun = {
        "pos" : [0.0, 0.0, 0,0],
        "vel" : [0.0, 0.0, 0,0],
        "mass" : 100000
    }

    earth = {
        "pos" : [100.0, 0.0, 0,0],
        "vel" : [0.0, 0.0, 0,0],
        "mass" : 1000
    }

    moon = {
        "pos" : [110.0, 0.0, 0,0],
        "vel" : [0.0, 0.0, 0,0],
        "mass" : 100
    }

    global bodies
    bodies = {"sun": sun, "sc": sc,"earth": earth, "moon": moon}
    while True:
        

        r = {}
        for i,body in enumerate(bodies):
        
            #print(body)     
            for other_body in bodies:
                if not body==other_body:
                    r[other_body] = np.linalg.norm(np.array(bodies[body]["pos"])-np.array(bodies[other_body]["pos"]))

        for i,body in enumerate(bodies):
            print(body)
            for other_body in bodies:
                if not body==other_body:
                    tmp = G * bodies[body]["mass"] / r[other_body]**3
                    acc = tmp * r[body]
                    vel = bodies[body]["vel"] + acc * dt
                    pos = bodies[body]["pos"] + vel * dt #symplectic, because we take already computed velocity
                    bodies[body]["pos"] = pos
                    print(pos)     

        time.sleep(dt)       

    
        

x = threading.Thread(target=push, args=())
x.start()

sim_thread = threading.Thread(target=sim_loop, args=())
sim_thread.start()



        
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
