class Subset():
    def __init__(self, *funct):
        for i in funct:
            if (callable(i)):
                self.__dict__[i.__name__] = i
