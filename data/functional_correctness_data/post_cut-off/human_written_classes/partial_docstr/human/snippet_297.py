import random
from syftr.configuration import NDIGITS

class RandomTrial:
    """A dummy trial class for generating random parameters."""

    def suggest_categorical(self, name, choices):
        return random.choice(choices)

    def suggest_int(self, name, low, high, step=1, log=False):
        return random.randrange(low, high + 1, step)

    def suggest_float(self, name, low, high, step=None, log=False):
        if step:
            num_steps = int((high - low) / step)
            return low + step * random.randint(0, num_steps)
        value = random.uniform(low, high)
        return round(value, NDIGITS)