# this class is the top level interface before the manager functions are called
from multiprocessing import Queue

from Boards.CMD.Interface import Interface as CMD
from Boards.Test.Interface import Interface as Test

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

    # returns queue of commands
    def get_commands(self):
        return self.q

    # called when entering
    def __enter__(self):
        # enter all iface members
        for i in self.iface:
            if (hasattr(i, '__enter__')):
                i.__enter__()
        return self

    # called when exiting
    def __exit__(self, e_type, e_value, e_traceback):
        # exit and join all iface members
        for i in self.iface:
            if (hasattr(i, '__exit__')):
                i.__exit__(e_type, e_value, e_traceback)

        for i in self.iface:
            i.join()
