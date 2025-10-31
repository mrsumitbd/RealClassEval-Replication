import time
from threading import Thread, Lock

class FIFOQueue:

    def __init__(self):
        self.queue = []
        self.lock = Lock()

    def push(self, item):
        with self.lock:
            self.queue.append(item)

    def pop(self):
        with self.lock:
            if self.queue:
                return self.queue.pop(0)
            return None

    def top(self):
        with self.lock:
            if self.queue:
                return self.queue[0]
            return None

    def next(self):
        while True:
            with self.lock:
                if self.queue:
                    return self.queue.pop(0)
            time.sleep(0.001)

    def clear(self):
        with self.lock:
            self.queue.clear()