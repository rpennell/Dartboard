import RPi.GPIO as GPIO
from multiprocessing import Queue

from Util import ShiftReg595, Collector, FaultThread

class Lights(FaultThread):
    def __init__(self, register_event):
        # exit event called when ready to exit
        self.exit = Event()
        # queue to put commands in
        self.cmd = Queue()

        # shift reg that goes to lights hardware
        self.shiftreg = ShiftReg595(10, 8, 7, 11, ["NC0", "White", "Red", "Enter", "Select", "Throw", "Remove", "NC1"])

        # call super and start thread
        super(Interface, self).__init__()
        self.start()

    def execute(self):
        # if we aren't exiting, keep running
        while not self.exit.is_set():
            sleep(THREAD_WAIT_TIME)

    def put(self, name, val, time=0):
        self.cmd.put

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        self.exit.set()
        self.join()

class ShiftReg595():
    def __init__(self, ser, oe, rclk, srclk, names=["a", "b", "c", "d", "e", "f", "g", "h"]):
        self.pins = Collector(ser=ser, oe=oe, rclk=rclk, srclk=srclk)
        self.names = OrderedDict((i, 0) for i in names[::-1])

        # initialize GPIO
        GPIO.setwarnings(False)
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

if __name__ == "__main__":
    reg = ShiftReg595(10, 8, 7, 11, ["NC0", "White", "Red", "ent_light", "sel_light", "throw_light", "remove_light", "NC1"])

    reg.set_all(1);
    raw_input()
    reg.set_all(0)
