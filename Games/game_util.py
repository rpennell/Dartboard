def point_lookup():
    points = {"Bullseye" : [25, 50]}
    for i in range(20):
        points[str(i+1)] = [i+1, 2*(i+1), 3*(i+1)]
    return points

class SetIterator():
    def __init__(self, index, mod):
        self.index = index
        self.mod = mod

    def __int__(self):
        return self.index/self.mod

    def __str__(self):
        return str(self.index) + " / " + str(self.mod)

    def next(self, success = None, overflow = None):
        self.index = (self.index + 1) % self.mod
        if (overflow != None and self.index == 0):
            overflow()
        if (success != None):
            success()
