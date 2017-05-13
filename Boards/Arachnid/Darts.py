import pigpio
#
# from Lights import *
#
# import RPi.GPIO as GPIO
# from time import sleep
# from threading import Thread
#
# class MatrixReader(Thread):
#     def __init__(self):
#         # initialize GPIO
#         GPIO.setwarnings(False)
#         GPIO.setmode(GPIO.BCM)
#
#         # Array of Columns as Outputs
#         self.COLS = [4, 17, 27, 22, 18, 23, 24, 25]
#
#         # Array of Rows as Inputs
#         self.ROWS = [12, 16, 20, 21, 6, 13, 19, 26]
#
#         self.SCORE = [
#             ["9 1",    "7 0",    "7 2",  "pass",       "9 0",  "9 2",  "7 1",  "14 2"],
#             ["13 1",   "17 0",   "17 2", "Bullseye 0", "13 0", "13 2", "17 1", "8 2" ],
#             ["11 1",   "20 0",   "20 2", "14 1",       "11 0", "11 2", "20 1", "14 0"],
#             ["10 1",   "18 0",   "18 2", "8 1",        "10 0", "10 2", "18 1", "8 0" ],
#             [ "5 1",   "12 0",   "12 2", "pass",       "5 0",  "5 0",  "12 1", "6 2" ],
#             [ "3 1",   "1 0",    "1 2",  "Bullseye 0", "3 0",  "3 2",  "1 1",  "15 2"],
#             [ "2 1",   "4 0",    "4 2",  "6 1",        "2 0",  "2 2",  "4 1",  "6 0" ],
#             ["16 1",   "19 0",   "19 2", "15 1",       "16 0", "16 2", "19 1", "15 0"],
#         ]
#
#         # set GPIOs to input/ouput
#         for i in self.COLS:
#             GPIO.setup(i, GPIO.OUT)
#             GPIO.output(i, GPIO.LOW)
#
#         for i in self.ROWS:
#             GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#
#         self.buffer = []
#         Thread.__init__(self)
#         self.daemon = True
#         self.start()
#
#     def get_reads(self):
#         temp = self.buffer
#         self.buffer = []
#         return temp
#
#     def run(self):
#         while True:
#             sleep(0.0000001)
#             for i in range(len(self.COLS)):
#                 GPIO.output(self.COLS[i], GPIO.HIGH)
#                 for j in range(len(self.ROWS)):
#                     if (GPIO.input(self.ROWS[j]) == 1):
#                         self.buffer.append(self.SCORE[i][j])
#                         sleep(0.5)
#                 GPIO.output(self.COLS[i], GPIO.LOW)
#
#     def __exit__(self):
#         GPIO.cleanup()

def cbf(gpio, level, tick):
   print(gpio, level, tick)

from time import sleep
if __name__ == '__main__':
    pi = pigpio.pi()             # exit script if no connection
    if not pi.connected:
       exit()
    x = [2, 3, 14, 15, 18]
    for i in x:
        pi.set_mode(i, pigpio.INPUT)
        pi.set_pull_up_down(i, pigpio.PUD_DOWN)
        pi.callback(i, pigpio.EITHER_EDGE, cbf)
    while True:
        pass
    # while True:
    #     print(pi.read(23))
    #     sleep(0.1)
    # try:
    #     reg = ShiftReg595(10, 8, 7, 11, ["NC0", "White", "Red", "ent_light", "sel_light", "throw_light", "remove_light", "NC1"])
    #
    #     reg.set_all(1);
    #
    #     pi = pigpio.pi()
    #     if not pi.connected:
    #        exit(0)

        # x = MatrixReader()
        # while True:
        #     sleep(10)
        #     for i in x.get_reads():
        #         print i
    # finally:
    #     reg.set_all(0)
