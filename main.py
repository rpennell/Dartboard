import Defaults

from time import sleep
from sys import exit
from importlib import import_module
from functools import partial

from Boards.SumInterface import SumInterface
from Manager import Manager
from Web import *

def loop():
    q = iface.get_commands()

    cmd_given = False
    while(not q.empty()):
        cmd_given = True
        manager.action(q.get())

    if cmd_given == True:
        update_all(manager.gui_data())

if __name__ == "__main__":
    manager = Manager()
    # TODO: make so defaults is passed to SumInterface
    with SumInterface(manager.events.register_event, manager.format_str) as iface:
        if (Defaults.Web_Enable):
            web_start(loop)
        else:
            while True:
                loop()
                # TODO: take out.  for testing only
                sleep(0.01)
