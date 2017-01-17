from functools import partial

from board_util import lookup, nada

class Decoder():

    def __init__(self, state, functions):
        if (state == "Options"):
            self.lookup = lookup(partial(nada))
            self.lookup["Enter"] = [partial(functions.nextcol)]
            self.lookup["Select"] = [partial(functions.shiftup)]

        elif (state == "Game"):
            self.lookup = lookup(partial(nada))
            self.lookup["Enter"] = [partial(functions.next_player)]
            self.lookup["Select"] = [partial(nada)]

            for i in self.lookup:
                if (hasattr(self.lookup[i], '__iter__') and len(self.lookup[i]) == 3):
                    for j in range(len(self.lookup[i])):
                        self.lookup[i][j] = partial(functions.throw_dart, i, j)

            self.lookup["Bullseye"] = [
                partial(functions.throw_dart, "Bullseye", 0),
                partial(functions.throw_dart, "Bullseye", 1),
            ]

        elif (state == "Winner"):
            self.lookup = lookup(partial(nada))
            self.lookup["Enter"] = [partial(functions.ready_to_exit)]
            self.lookup["Select"] = [partial(functions.ready_to_exit)]

        else:
            raise Exception("Invalid title for lookup table: " + str(state))

    def action(self, stream):
        actions = self.lookup.correlate(stream)
        for i in actions:
            i()
