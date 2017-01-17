import curses
from functools import partial
from json import dumps
from Web import update_all

from board_util import lookup, nada, COM

class Decoder():

    def __init__(self, state, functions):
        if (state == "Options"):
            self.lookup = lookup(partial(nada))
            self.lookup["enter"] = partial(functions.nextcol)
            self.lookup["select"] = partial(functions.shiftup)

            self.lookup["e"] = self.lookup["enter"]
            self.lookup["s"] = self.lookup["select"]


        elif (state == "Game"):
            self.lookup = lookup(partial(partial(functions.throw_dart)))
            self.lookup["enter"] = partial(functions.next_player)
            self.lookup["select"] = partial(nada)

            self.lookup["e"] = self.lookup["enter"]
            self.lookup["s"] = self.lookup["select"]

        elif (state == "Winner"):
            self.lookup = lookup(partial(nada))
            self.lookup["enter"] = partial(functions.ready_to_exit)
            self.lookup["select"] = partial(functions.ready_to_exit)

            self.lookup["e"] = self.lookup["enter"]
            self.lookup["s"] = self.lookup["select"]

        else:
            raise Exception("Invalid title for lookup table: " + str(state))

    def action(self, command):
        if (command in self.lookup):
            self.lookup[command]()

class Reader():

    def __init__(self, screen):
        self.screen = screen
        self.cmd = ""

    def refresh(self):
        self.screen.nodelay(1)
        inp = self.screen.getch()
        self.screen.nodelay(0)
        if (inp == curses.KEY_ENTER or inp == 10):
            temp = self.cmd
            self.cmd = ""
            return temp
        elif (inp != -1 and inp < 256):
            self.cmd += chr(inp)
        elif (inp == curses.KEY_BACKSPACE):
            self.cmd = self.cmd[:-1]

        return ""

    def current(self):
        return self.cmd

class Interface():
    def __init__(self):
        curses.cbreak
        self.screen = curses.initscr()
        self.reader = Reader(self.screen)
        (self.h, self.w) = self.screen.getmaxyx()
        self.screen.keypad(1)

        self.start_line = 5
        self.last_command = ""
        self.json = ""


    def refresh(self, manager):
        cmd = []
        cmd.append(self.reader.refresh())

        # go through list of commands
        run = True
        command_given = False
        for i in cmd:
            if (i != ""):
                self.last_command = i
                manager.action(i)
                command_given = True

        if (command_given or (self.json == "")):
            update_all(manager.gui_data())

        # redraw screen
        self.screen.clear()
        to_display = manager.format_str(level = 0, indent = "  ").split("\n")
        for i in range(0, self.h - self.start_line):
            if (len(to_display) > i):
                self.screen.addnstr(i + self.start_line, 0, to_display[i][:self.w], self.w)
            else:
                break
        self.screen.addnstr(3, 0, "GUI: " + str(manager.gui_data()), self.w)
        self.screen.addnstr(2, 0, "JSON: " + str(self.json), self.w)
        self.screen.addnstr(1, 0, "Last Command: " + self.last_command, self.w)
        self.screen.addnstr(0, 0, "Command: " + self.reader.current(), self.w)
        self.screen.refresh()

        return run

    def end(self):
        curses.endwin()
