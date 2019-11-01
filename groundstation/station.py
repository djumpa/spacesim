import socket
import time
import asyncio
import websockets

import signal
from multiprocessing import Value, Array, Process
from ctypes import c_char_p
class Groundstation:
    def __init__(self):
        self.host = 'localhost'
        self.port = 1234
        self.buf = 16384
        self.reply = Value(c_char_p, b"hello world")
        self.continue_run = Value('i',1)
        self.loop = asyncio.get_event_loop()  
        self.processes = []

    def run_server(self):
        print("groundstation run server thread initialized")
        signal.signal(signal.SIGINT, self.signal_handler)    
        start_server = websockets.serve(self.send_data, "localhost", 8765)
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()
        print("groundstation run server thread terminated")


    def run_client_socket(self):        
        signal.signal(signal.SIGINT, self.signal_handler)    
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((self.host, self.port))    
        clientsocket.send('test'.encode('utf-8'))

        print("groundstation thread initialized")
        while self.continue_run.value:
            self.reply = clientsocket.recv(self.buf)
        print("groundstation thread terminated")

    def run(self):    
        self.processes.append(Process(target=self.run_server).start())
        self.processes.append(Process(target=self.run_client_socket).start())

    def terminate(self):
        self.continue_run.value = 0    

    def signal_handler(self, sig, frame):
        for process in self.processes:
            if process and process.is_alive():
                process.terminate()    
     
    async def send_data(self,websocket, path):
        name = await websocket.recv()
        print(f"< {name}")

        while self.continue_run.value:
            await websocket.send(self.reply.value.decode())
            time.sleep(0.02)    
        self.loop.call_soon_threadsafe(self.loop.stop)       
        










