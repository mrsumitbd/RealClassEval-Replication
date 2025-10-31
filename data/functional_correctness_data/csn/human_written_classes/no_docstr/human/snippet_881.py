import numpy as np

class quality:

    def __init__(self, q):
        self.qual = [ord(value) for value in q]
        self.times = 1

    def update(self, q, counts=1):
        now = self.qual
        q = [ord(value) for value in q]
        self.qual = [x + y for x, y in zip(now, q)]
        self.times += counts

    def get(self):
        average = np.array(self.qual) / self.times
        return [str(unichr(int(char))) for char in average]