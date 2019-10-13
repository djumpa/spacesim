#!/usr/bin/env python3

import socket
import time
import asyncio
import websockets
import threading

host = 'localhost'
port = 1234
buf = 1024
reply = ''

def sock_client():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))

    print("Sending 'test'")
    clientsocket.send('test'.encode('utf-8'))
    print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))

    while True:
        try:
            
            global reply
            reply = clientsocket.recv(buf).decode('utf-8')
            if reply:
                print("REPLY: " + reply)
        except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
            print("Closing...")
            break

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"
    global reply

    await websocket.send(reply)
    print(f"> {greeting}")

x = threading.Thread(target=sock_client, args=())
x.start()

start_server = websockets.serve(hello, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()







