from importlib import import_module

from PlayerManager import PlayerManager
from Subset import Subset
from Games.game_util import SetIterator

class GameManager():

    # intialize the game with the specified number of players
    def __init__(self, game_name):
        self.settings = getattr(import_module("Games." + game_name), "options").collapse()

        self.players = PlayerManager(
            self.settings["Players"]
        )
        self.players.on_overflow(self.next_rnd)
        functions = Subset(
            self.players.__len__,
            self.players.index,
            self.players.next,
            self.players.on_player_change,
            self.players.on_overflow,
            self.players.player,
            self.players.to_dict,
        )
        self.settings.pop("Players")
        self.game = getattr(import_module(package + "." + game_name), game_name)(functions, **self.settings)
        self.rnd = 0

    def interface_data(self):
        if self.game.throw >= 3:
            return ["ent_light 1", "sel_light 0", "remove_light 0", "throw_light 0"]
        else:
            return ["ent_light 0", "sel_light 0", "remove_light 0", "throw_light 1"]

    def next_rnd(self):
        self.rnd += 1
        if (hasattr(self.game, 'on_round_change')):
            self.game.on_round_change(self.rnd)
        self.raise_event('round', self.rnd)

    def gui_data(self):
        temp = self.game.gui_data()
        temp["Round"] = self.rnd
        return temp

    # a dart was thrown.
    # @param: button - button dart hit
    #         mult - multiplyer hit
    # @return: true or false if throw is valid
    def throw_dart(self, button, mult):
        # TODO: add exit case exception
        button = str(button)
        mult = int(mult)
        if (button == "Bullseye" and (mult == 0 or mult == 1)):
            # for bullseye case
            pass
        elif (not (int(button) <= 20 and int(button) >= 1)):
            raise Exception("passed button value " + str(button) + "is not valid")
        elif (not (mult <= 2 and mult >= 0)):
            raise Exception("passed mult value " + str(mult) + "is not valid")
        self.game.throw_dart(button, mult)

    def allowed_functions(self):
        return Subset(
            self.throw_dart,
            self.game.next_player
        )


    # @return: name of winner if game is over.  None if game continues
    def exit_case(self):
        return self.game.winner

    def format_str(self, level = 0, indent = "   "):
        string = (indent * level) + "[\n"
        string += (indent * (level + 1)) + "Round: " + str(self.rnd) + "\n"
        string += (indent * (level + 1)) + "Game: \n"
        string += self.game.format_str(level + 2, indent)
        string += (indent * level) + "]\n"

        return string
