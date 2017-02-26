# this class is the top level interface before the manager functions are called
from multiprocessing import Queue

from Boards.CMD import Interface, Decoder

class SumInterface():
    def __init__(self):
        self.bufs = [
            ("CMD", Queue(), Decoder)
        ]
        self.iface = []
        for i in self.bufs:
            self.iface.append(Interface(i[1]))

    def refresh(self, functions):
        for i in self.bufs:
