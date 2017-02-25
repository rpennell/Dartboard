import Defaults

import curses
from functools import partial
from json import dumps
import RPi.GPIO as GPIO
from time import sleep, time

from Buttons import Buttons
from MatrixReader import MatrixReader
from Lights import ShiftReg595
from board_util import lookup, nada, COM

buff = []

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

class Hardware():
    def __init__(self):
        self.matrixReader = MatrixReader()
        self.buttons = Buttons()

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

    def refresh(self):
        global buff
        buff.extend(self.matrixReader.get_reads())
        buff.extend(self.buttons.get_reads())

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
        (self.h, self.w) = self.screen.getmaxyx()
        self.screen.keypad(1)

        self.start_line = 4
        self.last_command = ""
        self.json = ""
        self.lights = ""

    def refresh(self, manager, send):
        self.board.refresh()
        cmd = []
        cmd.append(self.reader.refresh())

        global buff
        self.screen.clear()

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
        self.board.end()
        curses.endwin()
