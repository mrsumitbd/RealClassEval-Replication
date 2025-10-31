import readchar

class KeyEventGenerator:

    def __init__(self, key_generator=None):
        self._key_gen = key_generator or readchar.readkey

    def next(self):
        return KeyPressed(self._key_gen())