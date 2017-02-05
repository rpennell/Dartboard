import RPi.GPIO as GPIO
from collections import OrderedDict
from time import sleep

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

    def __setitem__(self, key, value):
        self.names[key] = value
        self.update()

    def __getitem__(self, key):
        return self.name[key]

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

# lights = ShiftReg595(10, 8, 7, 11)
# # for i in range(8):
# #     lights.shift_in(1)
# #     lights.driver()
# #     sleep(1)
#
# lights["b"] = 1
# lights["c"] = 0
# lights["d"] = 0
# lights["e"] = 1
# sleep(1)
# lights["f"] = 1
