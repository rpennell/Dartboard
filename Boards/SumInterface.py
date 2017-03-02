# this class is the top level interface before the manager functions are called
from multiprocessing import Queue

from Boards.CMD.Interface import Interface as CMD
from Boards.Test.Interface import Interface as Test

# , Test.Interface


class SumInterface():
    def __init__(self):
        self.q = Queue()
        self.use = [Test]
        self.iface = []
        for i in self.use:
            self.iface.append(i(self.q))

    def refresh(self):
        for i in self.iface:
            i.refresh()

        # everything already in q
        return self.q

    def end(self):
        for i in self.iface:
            i.end()
