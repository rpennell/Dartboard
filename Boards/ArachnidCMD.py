import Defaults

import curses
from functools import partial
from threading import Timer,Thread,Event
from json import dumps
import RPi.GPIO as GPIO
import time

from board_util import lookup, nada, COM

buff = []

class perpetualTimer():

    def __init__(self,t,hFunction):
        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t,self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

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

class Edge():
    def __init__(self, returnable, ini=0):
        self.returnable = returnable
        self.last = ini

    def refresh(self, val):
        if ((val == 1) and (self.last == 0)):
            self.last = val
            return self.returnable
        else:
            self.last = val

class Hardware():
    def __init__(self):
        # Lookup table for score
        self.SCORE = [
            ["9 1",    "7 0",    "7 2",  "pass",       "9 0",  "9 2",  "7 1",  "14 2"],
            ["13 1",   "17 0",   "17 2", "Bullseye 0", "13 0", "13 2", "17 1", "8 2" ],
            ["11 1",   "20 0",   "20 2", "14 1",       "11 0", "11 2", "20 1", "14 0"],
            ["10 1",   "18 0",   "18 2", "8 1",        "10 0", "10 2", "18 1", "8 0" ],
            [ "5 1",   "12 0",   "12 2", "pass",       "5 0",  "5 0",  "12 1", "6 2" ],
            [ "3 1",   "1 0",    "1 2",  "Bullseye 0", "3 0",  "3 2",  "1 1",  "15 2"],
            [ "2 1",   "4 0",    "4 2",  "6 1",        "2 0",  "2 2",  "4 1",  "6 0" ],
            ["16 1",   "19 0",   "19 2", "15 1",       "16 0", "16 2", "19 1", "15 0"],
            ["enter",   "select", "pass",  "pass",       "pass", "pass", "pass", "pass"],
        ]
        for i in range(len(self.SCORE)):
            for j in range(len(self.SCORE[i])):
                self.SCORE[i][j] = Edge(self.SCORE[i][j])

        # Array of Rows
        self.ROWS = [3, 5, 7, 11, 13, 15, 19, 21, 40]

        # Array of Columns
        self.COLS = [23, 29, 31, 33, 18, 16, 35, 37]

        # Array of Light GPIOS
        # [enter, select, white, red, throw, remove]
        self.LIGHTS = {"ent_light": 32, "sel_light": 26, "throw_light": 12, "remove_light": 10}
        self.RED = 22
        self.WHITE = 24

        GPIO.setmode(GPIO.BOARD)

        for i in self.ROWS:
            GPIO.setup(i, GPIO.OUT)

        for i in self.COLS:
            GPIO.setup(i, GPIO.IN)

        for i in self.LIGHTS:
            GPIO.setup(self.LIGHTS[i], GPIO.OUT)

        for i in self.LIGHTS:
            GPIO.output(self.LIGHTS[i], GPIO.LOW)


        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.WHITE, GPIO.OUT)

        self.board_lights()

    def board_lights(self):
        GPIO.output(self.RED, GPIO.LOW)
        GPIO.output(self.WHITE, GPIO.HIGH)

    def light_switch(self, input):
        light = input.split()
        if (light[0] in self.LIGHTS):
            if light[1] == "0":
                GPIO.output(self.LIGHTS[light[0]], GPIO.LOW)
            else:
                GPIO.output(self.LIGHTS[light[0]], GPIO.HIGH)

    def refresh(self):
        global buff
        # stuff = False
        for i in range(len(self.ROWS)):
            GPIO.output(self.ROWS[i], GPIO.HIGH)
            for j in range(len(self.COLS)):
                temp =  self.SCORE[i][j].refresh(GPIO.input(self.COLS[j]))
                if temp != None:
                    time.sleep(Defaults.Debounce_Time)
                    buff.append(temp)
            GPIO.output(self.ROWS[i], GPIO.LOW)

    def end(self):
        for i in self.LIGHTS:
            GPIO.output(self.LIGHTS[i], GPIO.LOW)

        GPIO.output(self.RED, GPIO.LOW)
        GPIO.output(self.WHITE, GPIO.LOW)
        GPIO.cleanup()

class Interface():
    def __init__(self):
        curses.cbreak
        self.screen = curses.initscr()
        self.reader = Reader(self.screen)
        self.board = Hardware()
        self.timer = perpetualTimer(Defaults.Sample_Period, self.board.refresh)
        self.timer.start()
        (self.h, self.w) = self.screen.getmaxyx()
        self.screen.keypad(1)

        self.start_line = 4
        self.last_command = ""
        self.json = ""
        self.lights = ""

    def refresh(self, manager, send):
        cmd = []
        cmd.append(self.reader.refresh())

        global buff
        self.screen.clear()

        self.screen.addstr(3, 0, "Buffer: " + str(buff))

        for i in buff:
            cmd.append(i)
        buff = []

        # go through list of commands
        run = True
        command_given = False
        for i in cmd:
            if (i != ""):
                self.last_command = i
                manager.action(i)
                command_given = True
                if ((i == "enter" or i == "e")and manager.state.index == 1):
                    self.board.light_switch("throw_light 0")
                    self.board.light_switch("remove_light 1")
                    self.board.light_switch("enter_light 0")
                    self.update(manager, send)
                    time.sleep(Defaults.Recovery_Time)
                    # for i in ["ent_light 0", "sel_light 0", "remove_light 0", "throw_light 1"]:
                    #     self.board.light_switch(i)
                    buff = []


        self.lights = manager.interface_data()
        for i in self.lights:
            self.board.light_switch(i)

        if (command_given or (self.json == "")):
            self.update(manager, send)

        # redraw screen
        to_display = manager.format_str(level = 0, indent = "  ").split("\n")
        for i in range(0, self.h - self.start_line):
            if (len(to_display) > i):
                self.screen.addstr(i + self.start_line, 0, to_display[i][:self.w])
            else:
                break
        self.screen.addstr(4, 0, "JSON: " + str(self.json))
        self.screen.addstr(3, 0, "Buffer: " + str(buff))
        self.screen.addstr(2, 0, "Lights: " + str(self.lights))
        self.screen.addstr(1, 0, "Last Command: " + self.last_command)
        self.screen.addstr(0, 0, "Command: " + self.reader.current())
        self.screen.refresh()

        return run


    def update(self, manager, send):
        self.json = dumps(manager.gui_data())
        send(self.json)

    def end(self):
        self.timer.cancel()
        self.board.end()
        curses.endwin()
