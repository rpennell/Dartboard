from collections import deque

from debug_tools import *

class Options():

    def __init__(self, table = []):
        self.table = table
        self.generate()
        self._settings = {}

        # does this to load defaults into settings
        for i in self._options:
            self._settings[i[0]] = self._options[i[0]].popleft()[1].value

    def __iter__(self):
        for x in self._options:
            yield (x)

    def generate(self):
        self._options = dedict()

        for i in self.table:
            if (i.parent not in self._options):
                self._options[i.parent] = dedict()

            if (i.name not in self._options[i.parent]):
                self._options[i.parent].append(i.name, i)

        return self._options

    def collapse(self):
        for i in self._options:
            # only load valid options into settings
            try:
                self._settings[i[0]] = self._options[i[0]].popleft()[1].value
            except:
                pass

        return self._settings

class OptionsToken():
    def __init__(self, parent, name, value, cost, call = None):
        self.__dict__["parent"] = parent
        self.__dict__["name"] = name
        self.__dict__["value"] = value
        self.__dict__["cost"] = cost
        self.__dict__["call"] = call

    def __str__(self):
        return (
        "(" +
        str(self.__dict__["parent"]) + ", " +
        str(self.__dict__["name"]) + ", " +
        str(self.__dict__["value"]) + ", " +
        str(self.__dict__["cost"]) + ", " +
        str(self.__dict__["call"]) +
        ")"
        )


class dedict():
    def __init__(self, s = []):
        self._data = {}
        self._list = deque()

        for (k, v) in s:
            self.append(k, v)

    def append(self, key, value):
        if (key in self._data):
            raise KeyError('Key "' + str(key) + '" already exists')
        else:
            self._data[key] = value
            self._list.append(key)

    def keys(self):
        return list(self._list)

    def appendleft(self, key, value):
        if (key in self._data):
            raise KeyError('Key "' + str(key) + '" already exists')
        else:
            self._data[key] = value
            self._list.appendleft(key)

    def pop(self):
        key = self._list.pop()
        value = self._data[key]
        del self._data[key]
        return (key, value)

    def popleft(self):
        key = self._list.popleft()
        value = self._data[key]
        del self._data[key]
        return (key, value)

    def peek(self):
        return  (self._list[0], self._data[self._list[0]])

    def peekleft(self):
        return  (self._list[-1], self._data[self._list[-1]])

    def rotate(self, n):
        self._list.rotate(n)

    def __contains__(self, key):
        return key in self._data

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        for x in self._list:
            yield (x, self._data[x])

    def __setitem__(self, key, value):
        self._data[key] = value
        self._list.append(key)

    def format_str(self, level = 0, indent = "   "):
        string = (indent * level) + "[\n"
        for i in self._list:
            if (isinstance(self._data[i], dedict)):
                string += (indent * (level + 1)) + str(i) + ": " + self._data[i].format_str(level + 1, indent)
            else:
                string += (indent * (level + 1)) + str(i) + ": " + str(self._data[i]) + "\n"
        string += (indent * level) + "]\n"

        return string
