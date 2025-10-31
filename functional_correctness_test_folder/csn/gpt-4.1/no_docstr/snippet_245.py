
import random


class Sampleable:

    def __init__(self):
        self._samples = []
        self._default_sample = None

    def get_sample(self):
        if not self._samples:
            return self.get_default_sample()
        return random.choice(self._samples)

    def get_default_sample(self):
        return self._default_sample
