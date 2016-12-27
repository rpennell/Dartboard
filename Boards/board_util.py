from functools import partial

import socket               # Import socket module
import json

class COM():

    def __init__(self, mode):
        self.s = socket.socket()            # Create a socket object
        self.host = socket.gethostname()    # Get local machine name
        self.port = 1113                    # Reserve a port for your service.
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

class lookup(dict):
    def __init__(self, default=None, **kwargs):
        super(lookup, self).__init__()
        self["Bullseye 0"] = partial(default, "Bullseye", 0)
        self["Bullseye 1"] = partial(default, "Bullseye", 1)
        for i in range(20):
            for j in range(3):
                self[str(i+1) + " " + str(j)] = partial(default, str(i+1), j)

        for i in kwargs:
            self[i] = kwargs[i]

def nada(*args, **kwargs):
    pass

def print_function_lookup(x):
    for i in x:
        print("---" + str(i))
        for j in x[i]:
            if (isinstance(j, partial)):
                print_partial(j)
            else:
                print(j)

def print_partial(y):
    print(str(y.func) + " " + str(y.args) + " " + str(y.keywords))
