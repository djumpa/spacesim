import socket
import time
import asyncio
import websockets

import signal
from multiprocessing import Value, Array
from ctypes import c_char

class Groundstation:
    def __init__(self):
        self.host = 'localhost'
        self.port = 1234
        self.buf = 16384
        self.reply = Array(c_char, "")
        self.continue_run = Value('i',1)


    def run(self):    
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((self.host, self.port))    
        clientsocket.send('test'.encode('utf-8'))

        start_server = websockets.serve(self.hello, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

        print("groundstation thread initialized")
        def signal_handler(sig, frame):
            self.continue_run.value = 0

        while self.continue_run.value:
            self.reply.value = clientsocket.recv(self.buf).decode('utf-8')            

        signal.signal(signal.SIGINT, signal_handler)
        print("groundstation thread terminated")


    def terminate(self):
        self.continue_run.value = 0    
     


    async def hello(self,websocket, path):
        name = await websocket.recv()
        print(f"< {name}")

        while self.continue_run.value:
            await websocket.send(self.reply.value)
            time.sleep(0.02)









