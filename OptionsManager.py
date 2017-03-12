import importlib
import types

from Subset import Subset
from Options import *
from debug_tools import *

class OptionsManager():
    def __init__(self, raise_event, looped = False):
        self.raise_event = raise_event
        self.column = 0
        self.exit = None
        self.control_list = [
            ("Start", self.ready_to_exit)
        ]

        package = "Games"

        self.options = dedict()
        for i in getattr(importlib.import_module(package), "__all__"):
            self.options.append(i, getattr(importlib.import_module(package + "." + i), "options").generate())

        self._verify_options(self.options)

    def gui_data(self):
        temp = []
        try:
            temp.append(self.options.keys())
        except:
            temp.append([])

        try:
            temp.append(self.options.peek()[1].keys())
        except:
            temp.append([])

        try:
            temp.append(self.options.peek()[1].peek()[1].keys())
        except:
            temp.append([])

        return temp

    def format_str(self, level = 0, indent = "   "):
        return self.options.format_str(level, indent)

    def shiftup(self):
        self.get_column().rotate(-1)
        self.raise_event('up')

    def shiftdown(self):
        self.get_column().rotate(1)
        self.raise_event('down')

    def nextcol(self):
        nxt = self.get_column(1)
        if (isinstance(nxt, types.MethodType)):
            nxt()
        elif (not nxt == self.prevcol):
            self.column = (self.column + 1) % self.get_depth()
        self.raise_event('right')

    def prevcol(self):
        nxt = self.get_column(self.get_depth() - 1)
        self.column = (self.column - 1) % self.get_depth()
        self.raise_event('left')

    def get_depth(self):
        count = 0
        ptr = self.options
        while (isinstance(ptr, dedict)):
            count += 1
            ptr = ptr.peek()[1]

        return count

    def get_column(self, n = 0):
        ptr = self.options
        try:
            for i in range(self.column + n):
                ptr = ptr.peek()[1]
        except:
            raise IndexError("Index " + str(n) + " is out of bounds")

        return ptr

    def _verify_options (self, obj, level = 0):
        if (isinstance(obj, dedict)):
            if (level == 1):
                for (k, v) in self.control_list:
                    obj.append(k, v)
            for (k, v) in obj:
                self._verify_options(v, level + 1)

    def allowed_functions(self):
        return Subset(
            self.shiftup,
            self.shiftdown,
            self.nextcol,
            self.prevcol
        )

    def ready_to_exit(self):
        self.exit = True

    def exit_case(self):
        if (self.exit):
            game_name = self.options.peek()[0]
            return (game_name)
        else:
            return None
