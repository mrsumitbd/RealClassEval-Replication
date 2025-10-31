from itertools import tee

class TeeGenerator:
    """Stores a generator and calls ``tee`` on it to create new generators
    when ``TeeGenerator`` is iterated over to let you iterate over the given
    generator more than once.

    """

    def __init__(self, gen):
        self.gen = gen

    def __iter__(self):
        self.gen, it = tee(self.gen)
        yield from it