from time import time
from Util import FaultThread

class Interface(FaultThread):
    def __init__(self, q, register_event):
        self.q = q
        self.last = time()

    def execute(self):
        if (time() - self.last >= 1):
            self.q.put('pass')
            self.last = time()
