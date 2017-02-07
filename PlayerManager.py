from collections import OrderedDict

from Games.game_util import SetIterator

class PlayerManager(list):
    def __init__(self, players):
        super(PlayerManager, self).__init__("Player " + str(i) for i in range(1, players + 1))

        self._num = SetIterator(0, players)
        self._player_change = []
        self._overflow = []

    def to_dict(self, v = None):
        return OrderedDict((k, v) for k in self)

    def format_str(self, level = 0, indent = "   "):
        string = (indent * level) + "[\n"
        string += (indent * (level + 1)) + "Players: " + str(self) + "\n"
        string += (indent * level) + "]\n"

        return string

    def next(self):
        self._num.next(self._player_changes, self._overflows)

    def on_player_change(self, function):
        self._add_function(self._player_change, function)

    def on_overflow(self, function):
        self._add_function(self._overflow, function)

    def index(self):
        return self._num.index

    def player(self):
        return self[self.index()]

    def _add_function(self, lst, function):
        if (callable(function)):
            lst.append(function)
        else:
            raise Exception("Unsupported type passed: " + str(type(function)) + " must be a function")

    def _overflows(self):
        for i in self._overflow:
            i()

    def _player_changes(self):
        for i in self._player_change:
            i()
