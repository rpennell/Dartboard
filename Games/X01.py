from Options import Options, OptionsToken
from game_util import SetIterator, point_lookup

options = Options([
    OptionsToken("Players", "2", 2, (2, 0)),
    OptionsToken("Players", "3", 3, (3, 0)),
    OptionsToken("Players", "4", 4, (4, 0)),
    OptionsToken("Players", "1", 1, (1, 0)),
    OptionsToken("Score", "301", 301, (0, 0)),
    OptionsToken("Score", "501", 501, (2, 0)),
    OptionsToken("Score", "701", 701, (4, 0)),
])

class X01():
    # intialize the game with the specified number of players
    def __init__(self, pm, Score):
        self.point = point_lookup()
        self.pm = pm

        self.game = pm.to_dict(Score)

        self.busted = False
        self.bust_save = self.game[self.pm.player()]
        self.throw = 0

        self.winner = None

    def gui_data(self):
        temp = {
            "Name": self.__class__.__name__,
            "Throw": self.throw,
            "Players": self.game.keys(),
            "Scores": self.game.values(),
        }
        temp["Players"] = temp["Players"][-self.pm.index():] + temp["Players"][:-self.pm.index()]
        temp["Scores"] = temp["Scores"][-self.pm.index():] + temp["Scores"][:-self.pm.index()]
        return temp

    # is called whenever there is a player change from the GameManager
    def next_player(self):
        self.pm.next()
        self.busted = False
        self.bust_save = self.game[self.pm.player()]
        self.throw = 0

    # a dart was thrown.
    # @param: button - button dart hit
    #         mult - multiplyer hit
    # @return: true or false if throw is valid
    def throw_dart(self, button, mult):
        if (self.throw < 3):
            if (not self.busted):
                self.game[self.pm.player()] -= self.point[button][mult]
                self.throw += 1

            if (self.game[self.pm.player()] < 0):
                self.game[self.pm.player()] = self.bust_save
                self.busted = True

            elif (self.game[self.pm.player()] == 0):
                self.winner = self.pm.player()

    # @param: level - number of indents it needs to print
    #         indent - what each indent string should be
    # @return: a more terminal friendly string
    def format_str(self, level = 0, indent = "   "):
        string = (indent * level) + "Players: " + str(self.pm.player()) + "\n"
        string += (indent * level) + "Throw: " + str(self.throw) + " / 3\n"
        string += (indent * level) + str(self.game) + "\n"
        return string
