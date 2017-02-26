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
    iface.refresh(manager, update_all)

if __name__ == "__main__":
    manager = Manager()
    iface = SumInterface()
    try:


        if (Defaults.Web_Enable):
            web_start(loop)
        else:
            while True:
                loop()
                sleep(0.1)
    except KeyboardInterrupt:
        iface.end()
    finally:
        iface.end()

iface.end()
