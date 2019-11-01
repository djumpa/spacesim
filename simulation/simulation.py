import math
import socket
import time
import datetime
import numpy as np
import json

import signal
from multiprocessing import Value, Process

class Simulation:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 1234
        self.buf = 16384
        self.addr = (self.host, self.port)
        self.continue_run = Value('i',1)
        self.bodies = []
        self.clients = [self.serversocket]
        

    def run_handler(self, clientsocket, clientaddr):
        print("Accepted connection from: ", clientaddr)
    
        while self.continue_run.value:
            data = clientsocket.recv(1024)
            print(data.decode('utf-8'))
            if data.decode('utf-8') == "bye\n" or not data:
                break
            elif data.decode('utf-8') == "test1\n":
                clientsocket.send("test1\n".encode())
            else:
                clientsocket.send(("ECHO: " + data.decode('utf-8') + '\n').encode())

        self.clients.remove(clientsocket)
        clientsocket.close()
        print('Handler thread terminated')    

    def run_pipe(self):
        signal.signal(signal.SIGINT, self.signal_handler)  

        try:
            while self.continue_run.value: 
                for i in self.clients:
                    if i is not self.serversocket: # neposilat sam sobe            
                        i.send(json.dumps(self.bodies).encode())
                time.sleep(0.001)
        except ConnectionResetError:
            print("Connection ended on the otherside")
            exit
        print('Pipe thread terminated')        

    def run_server(self):    
        signal.signal(signal.SIGINT, self.signal_handler)  
        
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(self.addr)
        self.serversocket.listen(10)
        while self.continue_run.value:
            clientsocket, clientaddr = self.serversocket.accept()
            self.clients.append(clientsocket)
            Process(target= self.run_handler, args=(clientsocket, clientaddr)).start()
        self.serversocket.close()  
        print('Server thread terminated')          


    def run(self):
        # will run server
        # will run push thread

        signal.signal(signal.SIGINT, self.signal_handler)            
        dt = 10

        sc = {"position":[1.5e11+6971000,0,0], "mass":1, "velocity":[0,30000+8500,0], "name": "sc"}
        earth = {"position":[1.5e11,0,0], "mass":6e24, "velocity":[0,30000,0], "name": "earth",}
        sun = {"position":[0,0,0], "mass":2e30, "velocity":[0,0,0], "name": "sun"}
        moon = {"position":[1.5e11+384399000,0,0], "mass":7.3e22, "velocity":[0,30000+1000,0], "name": "moon"}

        self.bodies = [sun, earth, moon, sc]
        print('Simulation initialized')
        
        while self.continue_run.value:
            self.compute_gravity_step(self.bodies, time_step = dt)    
            time.sleep(0.02)
     
        print('Simulation thread terminated')    


    def terminate(self):
        self.continue_run.value = 0

    def signal_handler(self, sig, frame):
        self.continue_run.value = 0        

        
    def calculate_single_body_acceleration(self, bodies, body_index):
        G_const = 6.67408e-11  #m3 kg-1 s-2
        acceleration = [0,0,0]
        target_body = self.bodies[body_index]
        for index, external_body in enumerate(bodies):
            if index == body_index:
                continue

            r = (target_body["position"][0] - external_body["position"][0])**2 + \
                (target_body["position"][1] - external_body["position"][1])**2 + \
                (target_body["position"][2] - external_body["position"][2])**2
            r = math.sqrt(r)
            tmp = G_const * external_body["mass"] / r**3

            for i in range(0,3):    
                acceleration[i] += tmp * (external_body["position"][i] - target_body["position"][i])
        return acceleration    


    def compute_gravity_step(self, bodies, time_step = 1):
        for body_index, target_body in enumerate(self.bodies):
            acceleration = self.calculate_single_body_acceleration(self.bodies, body_index)

            for i in range(0,3):
                target_body["velocity"][i] += acceleration[i] * time_step
                target_body["position"][i] += target_body["velocity"][i] * time_step    