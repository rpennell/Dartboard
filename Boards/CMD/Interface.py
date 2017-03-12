import curses
from multiprocessing import Event
from time import sleep

from Util import FaultThread, probe
from Reader import Reader

class Interface(FaultThread):
    def __init__(self, q, register_event, debug_info):
        # exit event called when ready to exit
        self.exit = Event()
        # queue to put commands in
        self.q = q

        self.debug_info = debug_info
        self.event = ""
        register_event('all', self.event_call)

        # call super and start thread
        super(Interface, self).__init__()
        self.start()

    # overwritten execute of FaultThread
    def execute(self):
        # wrapper for curses that does friendlier error returns
        curses.wrapper(self.make_screen)

    # make curses screen
    def make_screen(self, stdscr):
        # set curses global parameters
        curses.use_default_colors()

        # save standard screen
        self.stdscr = stdscr
        with Reader(self.q, self.stdscr, self.current) as self.reader:

            # draw on standard screen
            (self.h, self.w) = self.stdscr.getmaxyx()
            self.stdscr.refresh()

            # if we aren't exiting, keep running
            self.refresh()
            while not self.exit.is_set():
                # self.refresh()
                sleep(0.5)

    # called when there is a new input character
    def current(self, current):
        self.stdscr.clrtoeol()
        self.stdscr.addnstr(0, 0, "Command: %s" % current, self.w)
        self.stdscr.refresh()

    # called when an event is called
    def event_call(self, *args, **kwargs):
        # turn event into string
        self.event = probe(*args, **kwargs)
        # refresh screen
        self.refresh()

    # refreshes terminal screen
    def refresh(self):
        # erase screen
        self.stdscr.erase()
        to_display = self.debug_info(level = 0, indent = "  ").split("\n")
        for i in range(0, self.h - 2):
            if (len(to_display) > i):
                self.stdscr.addnstr(i + 2, 0, to_display[i][:self.w], self.w)
            else:
                break
        self.stdscr.addnstr(1, 0, "Event: %s" % self.event, self.w)
        self.stdscr.refresh()

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        self.exit.set()
        self.reader.__exit__(e_type, e_value, e_traceback)
        self.join()
