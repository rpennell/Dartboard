from Subset import Subset

class WinnerManager():

    def __init__(self, winner):
        self.winner = winner
        self.exit = False

    def allowed_functions(self):
        return Subset(
            self.ready_to_exit
        )

    def interface_data(self):
        return ["ent_light 1", "sel_light 1", "remove_light 1", "throw_light 1"]

    def ready_to_exit(self):
        self.exit = True

    def gui_data(self):
        return [self.winner]

    def exit_case(self):
        if (self.exit == True):
            return True
        else:
            return None

    def format_str(self, level = 0, indent = "   "):
        string = (indent * level) + "[\n"
        string += (indent * (level + 1)) + "Winner: " + str(self.winner) + "\n"
        string += (indent * level) + "]\n"

        return string
