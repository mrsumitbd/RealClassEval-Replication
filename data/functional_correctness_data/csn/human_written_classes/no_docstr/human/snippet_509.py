import time

class BaseHelper:

    def __init__(self, verbose):
        self._start = time.time()
        self._debug = []
        if not verbose:
            self.debug = lambda *args: None

    def debug(self, *args):
        s = args[0] % args[1:]
        s = '[{}] {}'.format(str((time.time() - self._start) * 1000)[:5], s)
        self._debug.append(s)

    def report(self):
        for msg in self._debug:
            print(msg)