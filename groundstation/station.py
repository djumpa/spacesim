#!/usr/bin/env python3

import socket
import time
import asyncio
import websockets
import threading
import numpy as np
import json
import math

host = 'localhost'
port = 1234
buf = 32768
reply = ''

def sock_client():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))

    print("Starting send thread")
    clientsocket.send('test'.encode('utf-8'))
    #print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))

    while True:
        try:
            
            global reply
            reply = clientsocket.recv(buf).decode('utf-8')

            # Orbital parameters from https://space.stackexchange.com/questions/1904/how-to-programmatically-calculate-orbital-elements-using-position-velocity-vecto
            data = json.loads(reply)
            pos = np.array(data[1]["position"])-np.array(data[3]["position"])
            
            vel = np.array(data[1]["velocity"])-np.array(data[3]["velocity"])
            mu =data[1]["mu"]
            
            h = np.cross(pos,vel)
            n = np.cross(np.array([0,0,1]), h)
            evec = ((np.linalg.norm(vel)**2-mu/np.linalg.norm(pos))*pos-np.dot(pos,vel)*vel)/mu
            e = np.linalg.norm(evec)

            energy = np.linalg.norm(vel)**2/2-mu/np.linalg.norm(pos)

            eps = 1e-10
            if abs(e-1.0)>eps:
                a = -mu/(2*energy)
                p = a*(1-e**2)
            else:
                p = np.linalg.norm(h)**2/mu
                a = math.inf

            i = math.degrees(math.acos(h[2]/np.linalg.norm(h)))


            Omega = math.degrees(math.acos(n[0]/np.linalg.norm(n)))
           
            if n[1]<0:
                Omega = 360-Omega

            argp = math.degrees(math.acos(np.dot(n,evec)/(np.linalg.norm(n)*e)))

            if evec[2]<0:
                argp = 360-argp

            nu = math.degrees(math.acos(np.dot(evec,pos)/(e*np.linalg.norm(pos))))

            if np.dot(pos,vel) < 0 :
                nu = 360 - nu

            data[3]["orb"]={"e":e, "i": i, "a": a, "nu": nu, "omega": Omega, "argp": argp, "p":p}

            reply = json.dumps(data)

            #if reply:
                #print("REPLY: " + reply)
        except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
            print("Closing...")
            break

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    global reply
    while True:
        await websocket.send(reply)
        time.sleep(0.02)


x = threading.Thread(target=sock_client, args=())
x.start()

start_server = websockets.serve(hello, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()







