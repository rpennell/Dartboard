from time import time

class Interface():
    def __init__(self, q, register_event):
        self.q = q
        self.last = time()

    def refresh(self):
        if (time() - self.last >= 1):
            self.q.put('pass')
            self.last = time()
