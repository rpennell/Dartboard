from multiprocessing import Process, Queue, Event
from time import sleep, time

class test(Process):
    def __init__(self, t, q):
        self.exit = Event()
        self.t = t
        super(test, self).__init__()

    def run(self):
        while not self.exit.is_set():
            sleep(self.t)
            q.put(str(time()))

    def __exit__(self):
        self.exit.set()

q = Queue()
p = test(0.2, q)
p.start()
try:
    while True:
        while not q.empty():
            print q.get_nowait()
except KeyboardInterrupt:
    p.__exit__()
    p.join()
    sleep(1)
finally:
    p.__exit__()
    p.join()
    sleep(1)
