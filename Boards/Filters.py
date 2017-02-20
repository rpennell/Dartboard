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
