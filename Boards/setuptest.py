import RPi.GPIO as GPIO
LIGHTS = [32 ,26, 24, 22, 12, 10]
NAMES = ["enter", "select", "white", "red", "throw", "remove"]

GPIO.setmode(GPIO.BOARD)

for i in LIGHTS:
	GPIO.setup(i, GPIO.OUT)

def turn_on(light):
	length = range(len(LIGHTS))
	for i in length:
		if light == NAMES[i]:
			GPIO.output(LIGHTS[i], GPIO.HIGH)

def turn_off(light):
	length = range(len(LIGHTS))
	for i in length:
		if light == NAMES[i]:
			GPIO.output(LIGHTS[i], GPIO.LOW)

for i in NAMES:
	turn_on(i)

turn_off("white")