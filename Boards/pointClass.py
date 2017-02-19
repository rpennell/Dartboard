import RPi.GPIO as GPIO
from threading import Timer, Thread, Event
from time import sleep, time

class PerpetualTimer():
    def __init__(self, time, callback):
        self.time = time
        self.callback = callback
        self.thread = Timer(self.time, self.handle_function)

    def handle_function(self):
        self.callback()
        self.thread = Timer(self.time, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

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

class MatrixReader():
    def __init__(self):
        # initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

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

x = MatrixReader()
while True:
    temp = x.refresh()
    if (temp != None):
        print(temp)
