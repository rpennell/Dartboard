from time import sleep
from multiprocessing import Event

from Defaults import THREAD_WAIT_TIME
from Util import FaultThread

class Interface(FaultThread):
    def __init__(self, q, register_event):
        # exit event called when ready to exit
        self.exit = Event()
        # queue to put commands in
        self.q = q

        # call super and start thread
        super(Interface, self).__init__()
        self.start()

    def execute(self):
        # if we aren't exiting, keep running
        while not self.exit.is_set():
            sleep(THREAD_WAIT_TIME)

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        self.exit.set()
        self.join()
