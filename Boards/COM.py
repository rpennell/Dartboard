#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import json

class COM():

    def __init__(self, mode):
        self.s = socket.socket()            # Create a socket object
        self.host = socket.gethostname()    # Get local machine name
        self.port = 1110                    # Reserve a port for your service.
        if (mode == 'WRITE'):
            self.s.bind((self.host, self.port))       # Bind to the port
            self.s.listen(5)
            self.c, self.addr = self.s.accept()
        elif (mode == 'READ'):
            self.s.connect((self.host, self.port))

    def write(self, obj):
        # print(json.dumps(obj))
        self.c.send(json.dumps(obj))

    def read(self):
        msg = json.loads(self.s.recv(1024))
        # print(msg)
        return msg

    def close (self):
        self.s.close()
