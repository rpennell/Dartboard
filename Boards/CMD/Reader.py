import curses

from Defaults import KEYBOARD_TIMEOUT_MS
from Util import FaultThread

class Reader(FaultThread):
    def __init__(self, q, screen, current):
        self.current = current
        # curses screen
        self.screen = screen
        # leave timeout for input and don't echo to screen
        self.screen.timeout(KEYBOARD_TIMEOUT_MS)
        curses.noecho()
        
        # queue to put commands in
        self.q = q

        # place to put command
        self.cmd = ""

        super(Reader, self).__init__()

    # overwritten execute of FaultThread
    def execute(self):
        # loop to happen when not exiting
        while not self.exit.is_set():
            self.refresh()

    # gets and parses input characters
    def refresh(self):
        inp = self.screen.getch()
        # enter
        if (inp == curses.KEY_ENTER or inp == 10):
            self.q.put(self.cmd)
            self.cmd = ""
        # backspace
        elif (inp == curses.KEY_BACKSPACE):
            self.cmd = self.cmd[:-1]
        # value
        elif (inp != -1 and inp < 256):
            self.cmd += chr(inp)

        self.current(self.cmd)
