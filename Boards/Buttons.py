import RPi.GPIO as GPIO

class Buttons():
    def __init__(self, func):
        self.pins = [2, 3, 14, 15]

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for i in self.pins:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(i, GPIO.RISING, callback=func, bouncetime=300)

def printit(chan):
    print("Level detected on " + str(chan))

x = Buttons(printit)
while True:
    pass
