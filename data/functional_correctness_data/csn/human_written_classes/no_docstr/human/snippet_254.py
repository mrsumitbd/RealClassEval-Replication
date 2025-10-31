import threading

class Timer:

    def __init__(self, timeout, handler, args):
        self.timer = threading.Timer(timeout, handler, args)

    def start(self):
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    class TimeoutException(Exception):
        pass