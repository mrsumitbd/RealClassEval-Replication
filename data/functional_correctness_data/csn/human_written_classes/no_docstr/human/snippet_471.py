from numpy import random

class seeder:

    def __init__(self, func):
        self.func = func

    def __call__(self, **kwargs):
        seed = kwargs.pop('seed', None)
        if seed:
            random.seed(seed)
        return self.func(**kwargs)