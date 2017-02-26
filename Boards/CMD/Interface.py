import curses
from json import dumps

from Reader import Reader
from Web import update_all

class Interface():
    def __init__(self):
        curses.cbreak
        self.screen = curses.initscr()
        self.reader = Reader(self.screen)
        (self.h, self.w) = self.screen.getmaxyx()
        self.screen.keypad(1)

        self.start_line = 3
        self.last_command = ""
        self.json = ""


    def refresh(self, manager, send):
        cmd = []
        cmd.append(self.reader.refresh())

        # go through list of commands
        command_given = False
        for i in cmd:
            if (i != ""):
                self.last_command = i
                manager.action(i)
                command_given = True

        if (command_given):
            update_all(manager.gui_data())

        # redraw screen
        self.screen.clear()
        to_display = manager.format_str(level = 0, indent = "  ").split("\n")
        for i in range(0, self.h - self.start_line):
            if (len(to_display) > i):
                self.screen.addnstr(i + self.start_line, 0, to_display[i][:self.w], self.w)
            else:
                break
        self.screen.addnstr(2, 0, "JSON: " + str(self.json), self.w)
        self.screen.addnstr(1, 0, "Last Command: " + self.last_command, self.w)
        self.screen.addnstr(0, 0, "Command: " + self.reader.current(), self.w)
        self.screen.refresh()

    def end(self):
        curses.endwin()
