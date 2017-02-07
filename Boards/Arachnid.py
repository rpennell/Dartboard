import curses
from functools import partial

from board_util import lookup, nada, COM

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

def parse(state, command):
    command = command.split()
    if (len(command) == 1):
        if (command[0] == "select" or command[0] == "s"):
            state["Select"] = [True]
        elif (command[0] == "enter" or command[0] == "e"):
            state["Enter"] = [True]
        elif (command[0] == "pass"):
            pass
        elif (command[0] == "end" or command[0] == "exit"):
            return False
        # elif (command[0] == "preprog"):
        #     index_preprog = i
        elif (command[0] == "help"):
            print("   All commands are lower case")
            print("      exit - ends the program")
            print("      select - Select button on dartboard")
            print("      enter - Enter button on dartboard")
            print("      pass - do nothing")
            print("      preprog - use pre-programmed path")
            print("      num mult - throw dart at num in the space of the multiplier")
    elif (len(command) == 2):
        if (
            (command[0] in state) and
            (int(command[1]) < len(state[command[0]])) and
            (int(command[1]) >= 0)
        ):
            state[command[0]][int(command[1])] = True
    else:
        print("Invalid Command")
    return True

class Reader():

    def __init__(self, screen):
        self.screen = screen
        self.cmd = ""
        self.complete = False

    def refresh(self):
        self.screen.nodelay(1)
        inp = self.screen.getch()
        self.screen.nodelay(0)
        if (inp == curses.KEY_ENTER or inp == 10):
            self.complete = True
        elif (inp != -1 and inp < 256):
            self.cmd += chr(inp)
        elif (inp == curses.KEY_BACKSPACE):
            self.cmd = self.cmd[:-1]

    def current(self):
        return self.cmd

    def command(self):
        if (self.complete):
            self.complete = False
            temp = self.cmd
            self.cmd = ""
            return temp
        else:
            return str(0)

class Interface():
    def __init__(self):
        curses.cbreak
        self.screen = curses.initscr()
        self.reader = Reader(self.screen)
        (self.h, self.w) = self.screen.getmaxyx()
        self.screen.keypad(1)

        self.start_line = 1

    def refresh(self, manager):
        cmd = self.reader.refresh()
        self.screen.clear()
        to_display = manager.format_str(level = 0, indent = "  ").split("\n")
        for i in range(0, self.h - self.start_line):
            if (len(to_display) > i):
                self.screen.addstr(i + self.start_line, 0, to_display[i][:self.w])
            else:
                break
        self.screen.addstr(0, 0, "Command: " + self.reader.current())
        self.screen.refresh()

        x = self.reader.command()
        run = True
        if (x):
            state = lookup(False, Select = [False], Enter = [False])
            run = parse(state, x)
            manager.action(state)

        return run

    def end(self):
        curses.endwin()
