# this class is the top level interface before the manager functions are called
from multiprocessing import Queue

from Boards.CMD.Interface import Interface as CMD
from Boards.Test.Interface import Interface as Test

# , Test.Interface


class SumInterface():
    def __init__(self, register_event, debug_info):
        # queue for commands
        self.q = Queue()
        # interfaces
        self.use = [Test]
        # debugging interfaces
        self.debug = [CMD]
        # where declared interfces go
        self.iface = []

        # left uncombined for overhead
        for i in self.use:
            self.iface.append(i(self.q, register_event))
        for i in self.debug:
            self.iface.append(i(self.q, register_event, debug_info))

    def refresh(self):
        # refresh all interfaces
        for i in self.iface:
            i.refresh()

        # everything already in q
        return self.q

    # called when entering
    def __enter__(self):
        for i in self.iface:
            if (hasattr(i, '__enter__'))
                i.__enter__()

    # called when exiting
    def __exit__(self):
        for i in self.iface:
            if (hasattr(i, '__exit__'))
                i.__exit__()
