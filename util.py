from threading import Thread
from multiprocessing import Event, Queue
import sys

def probe(*args, **kwargs):
    delim = ", "
    event = delim.join(['%s' % i for i in args])
    if (args and kwargs):
        event += delim
    event += delim.join(['%s: %s' % (key, value) for (key, value) in kwargs.items()])
    return event

class Collector(dict):
    def __init__(self, *args, **kwargs):
        super(Collector, self).__init__(*args, **kwargs)
        self.__dict__ = self

class FaultThread(Thread):
    exc = Queue()

    def __init__(self):
        self.exit = Event()

        super(FaultThread, self).__init__()
        self.start()

    def execute(self):
        raise NotImplementedError

    @classmethod
    def ok(cls):
        return cls.exc.empty()

    def run(self):
        try:
            self.execute()
        except BaseException:
            exc = sys.exc_info()
            self.exc.put((exc[0], exc[1]))

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback, timeout=None):
        self.exit.set()
        self.join(timeout)

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
