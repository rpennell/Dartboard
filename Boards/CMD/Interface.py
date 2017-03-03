import curses
from json import dumps

from Reader import Reader
from Web import update_all

class Interface():
    def __init__(self, q, register_event, debug_info):
        self.q = q
        self.debug_info = debug_info

        curses.cbreak
        self.screen = curses.initscr()
        self.reader = Reader(self.screen)
        (self.h, self.w) = self.screen.getmaxyx()
        self.screen.keypad(1)

        self.start_line = 3
        self.last_command = ""
        self.json = ""
        self.event = ""

        register_event('all', self.event_call)

    def event_call(self, *args, **kwargs):
        # set event string to nothing then print passed args
        self.event = ""
        for i in args:
            self.event += str(i) + ", "
        for i in kwargs:
            self.event += str(i) + ": " + str(kwargs[i]) + ", "

    def refresh(self):
        self.q.put(self.reader.refresh())

        # redraw screen
        self.screen.clear()
        to_display = self.debug_info(level = 0, indent = "  ").split("\n")
        for i in range(0, self.h - self.start_line):
            if (len(to_display) > i):
                self.screen.addnstr(i + self.start_line, 0, to_display[i][:self.w], self.w)
            else:
                break
        self.screen.addnstr(2, 0, "Event: " + self.event, self.w)
        self.screen.addnstr(1, 0, "Last Command: " + self.last_command, self.w)
        self.screen.addnstr(0, 0, "Command: " + self.reader.current(), self.w)
        self.screen.refresh()

    def __exit__(self):
        curses.endwin()