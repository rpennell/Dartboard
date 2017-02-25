import Defaults

from time import sleep
from sys import exit
from importlib import import_module
from functools import partial

from Manager import Manager
from debug_tools import *
from Web import *

def loop():
    iface.refresh(manager, update_all)

if __name__ == "__main__":
    try:
        manager = Manager()
        iface = getattr(import_module("Boards." + Defaults.Interface_Type), "Interface")()

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
