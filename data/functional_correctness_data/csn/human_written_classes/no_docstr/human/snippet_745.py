from random import random

class Scope:

    def __init__(self, nmax=50, dt=0.1):
        self.dt = dt
        self.nmax = nmax
        self.tmax = dt * nmax
        self.t = []
        self.y = []

    def update(self):
        n = len(self.y)
        if n > self.nmax:
            self.t, self.y, n = ([0], [0], 1)
        self.t.append(n * self.dt)
        self.y.append(random() if random() < 0.15 else 0)
        return [(self.t, self.y)]