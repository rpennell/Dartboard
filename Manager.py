import Defaults
from importlib import import_module

from Decoder import Decoder
from OptionsManager import OptionsManager
from GameManager import GameManager
from WinnerManager import WinnerManager
from Games.game_util import SetIterator

class Manager():
    def __init__(self):
        self.all_managers = (
            ("Options", OptionsManager),
            ("Game", GameManager),
            ("Winner", WinnerManager)
        )
        self.events = Events()
        self.state = SetIterator(0, len(self.all_managers))
        self.manager = self.all_managers[self.state.index][1](self.events.raise_event)
        self.decoder = Decoder(self.all_managers[self.state.index][0], self.manager.allowed_functions())

    def action(self, command):
        self.decoder.action(command)

        val_to_pass = self.manager.exit_case()
        if (val_to_pass != None):
            self.state.next()
            self.manager = self.all_managers[self.state.index][1](self.events.raise_event, val_to_pass)
            self.decoder = Decoder(self.all_managers[self.state.index][0], self.manager.allowed_functions())
            self.events.raise_event('state', self.all_managers[self.state.index][0])

    def gui_data(self):
        return {
            "State": self.all_managers[self.state.index][0],
            "Data": self.manager.gui_data()
        }

    def format_str(self, level = 0, indent = "    "):
        string = (indent * level) + "Manager State: " + self.all_managers[self.state.index][0] + "\n"
        string += self.manager.format_str(level + 1, indent)

        return string

class Events(dict):
    def __init__(self):
        super(Events, self).__init__()

        # Initialize all known events___________________________________________

        # Called: after any other event is called
        # Param: event type, anything passed in event
        self['all'] = []

        # Called: on state change
        # Param: current state
        self['state'] = []

        # Called: on up
        self['up'] = []

        # Called: on down
        self['down'] = []

        # Called: on left
        self['left'] = []

        # Called: on right
        self['right'] = []

        # Called: on throw
        # Param: throw number
        self['throw'] = []

        # Called: when you've thrown too many or internal game reasons (bust)
        self['throw_invalid'] = []

        # Called: on a player change
        # Param: current player name
        self['player'] = []

        # Called: on a round change
        # Param: current round number
        self['round'] = []

    def register_event(self, key, function):
        if (key in self):
            if callable(function) == True:
                self[key].append(function)
            else:
                raise Exception("function must be callable")
        else:
            raise Exception('Must register valid event')

    def raise_event(self, key, *args, **kwargs):
        if (key in self):
            for i in self[key]:
                i(*args, **kwargs)
            for i in self['all']:
                i(key, *args, **kwargs)
        else:
            raise Exception('Must raise valid event')
