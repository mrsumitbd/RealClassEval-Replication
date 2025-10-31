import time
import sys

class Progress:

    def __init__(self):
        self._current_text = ''

    def write(self, string, withLazy=False):
        self._current_text = str(string)
        sys.stdout.write('\r' + '\x1b[32mMirage: \x1b[0m' + str(self._current_text))
        if withLazy:
            time.sleep(0.5)

    def update(self, string, withLazy=False):
        sys.stdout.flush()
        sys.stdout.write('\r{0}'.format('                                                                               '))
        sys.stdout.flush()
        self.write(string, withLazy)

    def clear(self):
        sys.stdout.flush()
        sys.stdout.write('\r{0}'.format('                                                                               '))