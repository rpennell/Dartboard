"""
This program does the conversion of the dartboard matrix to the actual point value.
"""

import RPi.GPIO as GPIO
import time

# Rows of matrix (OUTPUTS)
R0 = 3
R1 = 5
R2 = 7
R3 = 11
R4 = 13
R5 = 15
R6 = 19
R7 = 21

# Columns of Matrix (INPUTS)
colA = 23
colB = 29
colC = 31
colD = 33
colE = 35
colF = 37
colG = 8
colH = 10

# Array of Rows
ROWS = [R0, R1, R2, R3, R4, R5, R6, R7]

# Array of Columns
COLS = [colA, colB, colC, colD, colE, colF, colG, colH]

# The rows represent the numbers 0-7 and the columns are represented by the letters A-H
# The point value and multiplier are stored in the corresponding index of the matrix
# The first number is the point and the second is the multiplier
scoreMatrix = [[[9, 2],  [7, 1],  [7, 3],  [0, 0],  [9, 1],  [9, 3],  [7, 2],  [14, 3]],
               [[13, 2], [17, 1], [17, 3], [25, 1], [13, 1], [13, 3], [17, 2], [8, 3]],
               [[11, 2], [20, 1], [20, 3], [14, 2], [11, 1], [11, 3], [20, 2], [14, 1]],
               [[10, 2], [18, 1], [18, 3], [8, 2],  [10, 1], [10, 3],  [18, 2], [8, 1]],
               [[5, 2],  [12, 1], [12, 3], [0, 0],  [5, 1],  [5, 3],  [12, 2], [6, 3]],
               [[3, 2],  [1, 1],  [1, 3],  [50, 1], [3, 1],  [3, 3],  [1, 2],  [15, 3]],
               [[2, 2],  [4, 1],  [4, 3],  [6, 2],  [2, 1],  [2, 3],  [4, 2],  [6, 1]],
               [[16, 2], [19, 1], [19, 3], [15, 2], [16, 1], [16, 3], [19, 2], [15, 1]]]

# This method returns a pa
def scoreReturn(row, col):
    return scoreMatrix[row][col]

# This method configures the GPIOs into the correct I/O settings
def gpioConfig():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(R0, GPIO.OUT)
    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)
    GPIO.setup(R5, GPIO.OUT)
    GPIO.setup(R6, GPIO.OUT)
    GPIO.setup(R7, GPIO.OUT)
    GPIO.setup(colA, GPIO.IN)
    GPIO.setup(colB, GPIO.IN)
    GPIO.setup(colC, GPIO.IN)
    GPIO.setup(colD, GPIO.IN)
    GPIO.setup(colE, GPIO.IN)
    GPIO.setup(colF, GPIO.IN)
    GPIO.setup(colG, GPIO.IN)
    GPIO.setup(colH, GPIO.IN)


# Returns a list of the buttons pressed from the dartboard. Each element is stored as a score and multiplier pair
def recordThrow():
    R = range(len(ROWS))
    C = range(len(COLS))
    buttons = []
    for i in R:
        GPIO.output(ROWS[i], GPIO.HIGH)
        for j in C:
            time.sleep(0.01)
            if GPIO.input(COLS[j]):
                GPIO.output(ROWS[i],GPIO.LOW)
                buttons.append(scoreMatrix[i][j])
        GPIO.output(ROWS[i], GPIO.LOW)
    return buttons

gpioConfig()
while 1:
  list = recordThrow()
  print list




