# this class is the top level interface before the manager functions are called
from multiprocessing import Queue

from Boards.CMD.Interface import Interface as CMD
from Boards.Test.Interface import Interface as Test

# , Test.Interface


class SumInterface():
    def __init__(self, get_state):
        self.q = Queue()
        self.use = [Test]
        self.debug = [CMD]
        self.iface = []

        # left uncombined for overhead
        for i in self.use:
            self.iface.append(i(self.q))
        for i in self.debug:
            self.iface.append(i(self.q, get_state))

    def refresh(self):
        # refresh all interfaces
        for i in self.iface:
            i.refresh()

        # everything already in q
        return self.q

    def end(self):
        for i in self.iface:
            i.end()
