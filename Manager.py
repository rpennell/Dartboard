import Defaults
from importlib import import_module

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
        self.state = SetIterator(0, len(self.all_managers))
        self.manager = self.all_managers[self.state.index][1]()
        self.decoder = getattr(import_module("Boards." + Defaults.Interface_Type), "Decoder")(self.all_managers[self.state.index][0], self.manager.allowed_functions())

    def interface_data(self):
        return self.manager.interface_data()

    def action(self, command):
        self.decoder.action(command)

        val_to_pass = self.manager.exit_case()
        if (val_to_pass != None):
            self.state.next()
            self.manager = self.all_managers[self.state.index][1](val_to_pass)
            self.decoder = getattr(import_module("Boards." + Defaults.Interface_Type), "Decoder")(self.all_managers[self.state.index][0], self.manager.allowed_functions())

    def gui_data(self):
        return {
            "State": self.all_managers[self.state.index][0],
            "Data": self.manager.gui_data()
        }

    def format_str(self, level = 0, indent = "    "):
        string = (indent * level) + "Manager State: " + self.all_managers[self.state.index][0] + "\n"
        string += self.manager.format_str(level + 1, indent)

        return string
