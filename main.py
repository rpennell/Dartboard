import Defaults

from time import sleep
from sys import exit
from importlib import import_module
from functools import partial

from Boards.SumInterface import SumInterface
from Manager import Manager
from debug_tools import *
from Web import *

def loop():
    q = iface.refresh()

    cmd_given = False
    while(not q.empty()):
        cmd_given = True
        manager.action(q.get())

    if cmd_given == True:
        pass
        # update_all(manager.interface_data()["State"])

if __name__ == "__main__":
    manager = Manager()
    # TODO: make so defaults is passed to SumInterface
    iface = SumInterface(manager.events.register_event, manager.format_str)
    iface.refresh()

    try:
        if (Defaults.Web_Enable):
            web_start(loop)
        else:
            while True:
                loop()
                # TODO: take out.  for testing only
                sleep(0.01)
    except KeyboardInterrupt:
        iface.end()
    finally:
        iface.end()

iface.end()
