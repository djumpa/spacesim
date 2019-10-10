#!/usr/bin/env python3

import socket
import time
import asyncio
import websockets

host = 'localhost'
port = 1234
buf = 1024

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))

print("Sending 'test1\\n'")
clientsocket.send('test1\n'.encode('utf-8'))
print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))

print("Sending 'test2'")
clientsocket.send('test2'.encode('utf-8'))
print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))

print("Sending 'abc'")
clientsocket.send('abc'.encode('utf-8'))
print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))

print("Sending 'abc'")
clientsocket.send('abc'.encode('utf-8'))
print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))

print("Sending 'bye'")
clientsocket.send('bye\n'.encode('utf-8'))
print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))

while True:
    try:
        time.sleep(1)
        print("REPLY: " + clientsocket.recv(buf).decode('utf-8'))
    except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
        print("Closing...")
        break

