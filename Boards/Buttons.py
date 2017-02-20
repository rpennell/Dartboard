import RPi.GPIO as GPIO
from time import sleep

class Buttons():
    def __init__(self):
        self.pins = {
            str(2): "pass",
            str(3): "pass",
            str(14): "select",
            str(15): "enter"
        }
        self.buffer = []

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for i in self.pins:
            GPIO.setup(int(i), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(int(i), GPIO.RISING, callback=self.pressed, bouncetime=500)

    def get_reads(self):
        temp = self.buffer
        self.buffer = []
        return temp

    def pressed(self, chan):
        self.buffer.append(self.pins[str(chan)])

if __name__ == "__main__":
    x = Buttons()
    while True:
        for i in x.get_reads():
            print(i)
            sleep(0.1)
