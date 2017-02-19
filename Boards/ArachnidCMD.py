import Defaults

import curses
from functools import partial
from threading import Timer, Thread, Event
from json import dumps
import RPi.GPIO as GPIO
from collections import OrderedDict
from time import sleep, time

from board_util import lookup, nada, COM

buff = []

class Collector(dict):
    def __init__(self, *args, **kwargs):
        super(Collector, self).__init__(*args, **kwargs)
        self.__dict__ = self

class ShiftReg595():
    def __init__(self, ser, oe, rclk, srclk, names=["a", "b", "c", "d", "e", "f", "g", "h"]):
        self.pins = Collector(ser=ser, oe=oe, rclk=rclk, srclk=srclk)
        self.names = OrderedDict((i, 0) for i in names[::-1])

        GPIO.setmode(GPIO.BCM)
        for i in self.pins:
            GPIO.setup(self.pins[i], GPIO.OUT)

        self.set_all(0)
        self.output_enable(1)

    def __getitem__(self, key):
        return self.name[key]

    def __iter__(self):
        return self.names.__iter__()

    def __setitem__(self, key, value):
        self.names[key] = value
        self.update()

    def driver(self):
        GPIO.output(self.pins.rclk, 1)
        sleep(0.000000094)
        GPIO.output(self.pins.rclk, 0)

    def output_enable(self, en):
        GPIO.output(self.pins.oe, not en)

    # sets value to be shifted but does not shift the value into the register
    def place(self, key, value):
        self.names[key] = value

    def set_all(self, inp):
        for i in self.names:
            self.names[i] = inp
            self.shift_in(self.names[i])

        self.driver()

    def shift_in(self, inp):
        # shift a zero in
        GPIO.output(self.pins.ser, inp)
        sleep(0.000000125)
        GPIO.output(self.pins.srclk, 1)
        sleep(0.0000001)
        GPIO.output(self.pins.srclk, 0)

    def update(self):
        for i in self.names:
            self.shift_in(self.names[i])

        self.driver()

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

class SensorFilter():
    def __init__(self, returnable, initial=0, samples=10):
        self.ones = samples * initial
        self.samples = samples
        self.last = initial
        self.returnable = returnable

    def refresh(self, val):
        if (self.edge(self.average(val)) == 1):
            return self.returnable
        return None

    def average(self, val):
        if ((val == 0) and (self.ones >= 0)):
            self.ones -= 1
        elif ((val == 1) and (self.ones < self.samples)):
            self.ones += 1

        if (self.ones > self.samples/2):
            return 1
        else:
            return 0

    def edge(self, val):
        if ((val == 1) and (self.last == 0)):
            self.last = val
            return 1
        self.last = val
        return 0

class Buttons():
    def __init__(self, func):
        self.pins = [2, 3, 14, 15]

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for i in self.pins:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(i, GPIO.RISING, callback=func, bouncetime=300)

class MatrixReader():
    def __init__(self):
        # initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Array of Columns as Outputs
        self.COLS = [4, 17, 27, 22, 18, 23, 24, 25]

        # Array of Rows as Inputs
        self.ROWS = [12, 16, 20, 21, 6, 13, 19, 26]

        self.SCORE = [
            ["9 1",    "7 0",    "7 2",  "pass",       "9 0",  "9 2",  "7 1",  "14 2"],
            ["13 1",   "17 0",   "17 2", "Bullseye 0", "13 0", "13 2", "17 1", "8 2" ],
            ["11 1",   "20 0",   "20 2", "14 1",       "11 0", "11 2", "20 1", "14 0"],
            ["10 1",   "18 0",   "18 2", "8 1",        "10 0", "10 2", "18 1", "8 0" ],
            [ "5 1",   "12 0",   "12 2", "pass",       "5 0",  "5 0",  "12 1", "6 2" ],
            [ "3 1",   "1 0",    "1 2",  "Bullseye 0", "3 0",  "3 2",  "1 1",  "15 2"],
            [ "2 1",   "4 0",    "4 2",  "6 1",        "2 0",  "2 2",  "4 1",  "6 0" ],
            ["16 1",   "19 0",   "19 2", "15 1",       "16 0", "16 2", "19 1", "15 0"],
        ]

        # set GPIOs to input/ouput
        for i in self.COLS:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.LOW)

        for i in self.ROWS:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for i in range(len(self.COLS)):
            for j in range(len(self.ROWS)):
                self.SCORE[i][j] = SensorFilter(self.SCORE[i][j])

        self.charge_time = 0.0000001
        self.debounce_time = 0.1
        self.last = time()

    def refresh(self):
        val = None
        for i in range(len(self.COLS)):
            GPIO.output(self.COLS[i], GPIO.HIGH)
            sleep(self.charge_time)
            for j in range(len(self.ROWS)):
                x = self.SCORE[i][j].refresh(GPIO.input(self.ROWS[j]))
                if x != None:
                    if (time() - self.last >= self.debounce_time):
                        self.last = time()
                        val = x
            GPIO.output(self.COLS[i], GPIO.LOW)
            sleep(self.charge_time)

        return val

    def __exit__(self):
        GPIO.cleanup()

class Hardware():
    def __init__(self):
        self.matrixReader = MatrixReader()
        self.buttons = Buttons(self.button_func)

        # Array of Light GPIOS
        self.lights = ShiftReg595(10, 8, 7, 11, ["NC0", "White", "Red", "ent_light", "sel_light", "throw_light", "remove_light", "NC1"])

        self.board_lights()

    def board_lights(self):
        self.lights["White"] = 1
        self.lights["Red"] = 0

    def light_switch(self, input):
        light = input.split()
        if (light[0] in self.lights):
            if light[1] == "0":
                self.lights[light[0]] = 0
            elif light[1] == "1":
                self.lights[light[0]] = 1

    def button_func(self, chan):
        global buff

        if chan == 2:
            buff.append("pass")
        elif chan == 3:
            buff.append("pass")
        elif chan == 14:
            buff.append("select")
        elif chan == 15:
            buff.append("enter")

    def refresh(self):
        global buff
        x = self.matrixReader.refresh()
        if x != None:
            buff.append(x)
        # global buff
        # stuff = False
        # for i in range(len(self.ROWS)):
        #     GPIO.output(self.ROWS[i], GPIO.HIGH)
        #     for j in range(len(self.COLS)):
        #         temp =  self.SCORE[i][j].refresh(GPIO.input(self.COLS[j]))
        #         if temp != None:
        #             sleep(Defaults.Debounce_Time)
        #             buff.append(temp)
        #     GPIO.output(self.ROWS[i], GPIO.LOW)

    def end(self):
        for i in self.lights:
            self.lights[i] = 0

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
                    sleep(Defaults.Recovery_Time)
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
