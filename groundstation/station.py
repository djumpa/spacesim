#!/usr/bin/env python3

import socket
import time

host = 'localhost'
port = 1234
buf = 1024

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
        break
        print("Closing...")


