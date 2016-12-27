from Options import Options, OptionsToken
from game_util import SetIterator, point_lookup

options = Options([
    OptionsToken("Players", "2", 2, (2, 0)),
    OptionsToken("Players", "3", 3, (3, 0)),
    OptionsToken("Players", "4", 4, (4, 0)),
    OptionsToken("Players", "1", 1, (1, 0)),
    # OptionsToken("Bullseye", "Yes", True, (0, 0)),
    # OptionsToken("Bullseye", "No", False, (0, 0)),
    # OptionsToken("Count", "All", 0, (0, 0)),
    # OptionsToken("Count", "Doubles and Triples", 1, (1, 0)),
    # OptionsToken("Count", "Triples", 2, (2, 0)),
    OptionsToken("Lives", "7", 7, (0, 0)),
    OptionsToken("Lives", "8", 8, (0, 0)),
    OptionsToken("Lives", "9", 9, (0, 0)),
    OptionsToken("Lives", "10", 10, (0, 1)),
    OptionsToken("Lives", "11", 11, (0, 1)),
    OptionsToken("Lives", "12", 12, (0, 1)),
    OptionsToken("Lives", "13", 13, (0, 1)),
    OptionsToken("Lives", "14", 14, (0, 1)),
    OptionsToken("Lives", "15", 15, (0, 1)),
    OptionsToken("Lives", "1", 1, (0, 0)),
    OptionsToken("Lives", "2", 2, (0, 0)),
    OptionsToken("Lives", "3", 3, (0, 0)),
    OptionsToken("Lives", "4", 4, (0, 0)),
    OptionsToken("Lives", "5", 5, (0, 0)),
    OptionsToken("Lives", "6", 6, (0, 0)),
])

class Battleship():
    # intialize the game with the specified number of players
    def __init__(self, functions, Lives):
        self.game = []
        self.functions = functions

        for i in range(self.functions.total_players()):
            self.game.append(1)

        self.winner = None
        self.throw = 0

    # is called whenever there is a player change from the GameManager
    def next_player(self):
        self.functions.next()
        self.throw = 0

    # a dart was thrown.
    # @param: button - button dart hit
    #         mult - multiplyer hit
    # @return: true or false if throw is valid
    def throw_dart(self, button, mult):
        if (self.throw < 3):
            self.throw += 1

    # @param: level - number of indents it needs to print
    #         indent - what each indent string should be
    # @return: a more terminal friendly string
    def format_str(self, level = 0, indent = "   "):
        string = (indent * level) + "Players: " + str(self.functions.get_player()) + " / " + str(self.functions.total_players()) + "\n"
        string += (indent * level) + "Throw: " + str(self.throw) + " / 3\n"
        string += (indent * level) + str(self.game) + "\n"
        return string
