#!/usr/bin/env python3

import math
import socket
import threading
import time
import datetime
import numpy as np
import json


host = '0.0.0.0'
port = 1234
buf = 16384

addr = (host, port)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(addr)
serversocket.listen(10)

clients = [serversocket]

bodies = []
def calculate_single_body_acceleration(bodies, body_index):
    G_const = 6.67408e-11  #m3 kg-1 s-2
    acceleration = [0,0,0]
    target_body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (target_body["position"][0] - external_body["position"][0])**2 + (target_body["position"][1] - external_body["position"][1])**2 + (target_body["position"][2] - external_body["position"][2])**2
            r = math.sqrt(r)
            tmp = G_const * external_body["mass"] / r**3
            acceleration[0] += tmp * (external_body["position"][0] - target_body["position"][0])
            acceleration[1] += tmp * (external_body["position"][1] - target_body["position"][1])
            acceleration[2] += tmp * (external_body["position"][2] - target_body["position"][2])

    return acceleration

def compute_gravity_step(bodies, time_step = 1):
    for body_index, target_body in enumerate(bodies):
        acceleration = calculate_single_body_acceleration(bodies, body_index)

        target_body["velocity"][0] += acceleration[0] * time_step
        target_body["velocity"][1] += acceleration[1] * time_step
        target_body["velocity"][2] += acceleration[2] * time_step 

        target_body["position"][0] += target_body["velocity"][0] * time_step
        target_body["position"][1] += target_body["velocity"][1] * time_step
        target_body["position"][2] += target_body["velocity"][2] * time_step

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
        print("Start of push thread")
        while True: 
            for i in clients:
                if i is not serversocket: # neposilat sam sobe
                    #print(bodies)
                    i.send(json.dumps(bodies).encode())
            time.sleep(0.001) # [s]
    except ConnectionResetError:
        print("Connection ended on the otherside")
        exit

def sim_loop():
    print("Start of sim thread")
    # Inital conditions and constants

    dt = 100

    sc = {"position":[1.5e11+7000000,0,0], "mass":1, "velocity":[0,30000+3000,0], "name": "sc"}
    earth = {"position":[1.5e11,0,0], "mass":6e24, "velocity":[0,30000,0], "name": "earth",}
    sun = {"position":[0,0,0], "mass":2e30, "velocity":[0,0,0], "name": "sun"}
    moon = {"position":[1.5e11+384399000,0,0], "mass":7.3e22, "velocity":[0,30000+1000,0], "name": "moon"}

    global bodies
    bodies = [sun, earth, moon, sc]


    while True:
        compute_gravity_step(bodies, time_step = dt)    
        time.sleep(0.04)
    
        

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
