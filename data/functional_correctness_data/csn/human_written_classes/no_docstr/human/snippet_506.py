import numpy as np
import sys
import random

class Particle:

    def __init__(self, bounds):
        self.ndim = len(bounds)
        self.velocity = np.random.uniform(-1, 1, self.ndim)
        self.position = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
        self.best_pos = self.position
        self.best_score = sys.float_info.max
        self.score = sys.float_info.max

    def evaluate(self, cost_func):
        self.score = cost_func(self.position)
        if self.score < self.best_score:
            self.best_pos = self.position
            self.best_score = self.score

    def update_velocity(self, best_position_global, w, c1, c2):
        r1 = random.random()
        r2 = random.random()
        vc = c1 * r1 * (self.best_pos - self.position)
        vs = c2 * r2 * (best_position_global - self.position)
        self.velocity = w * self.velocity + vc + vs

    def update_position(self, bounds):
        self.position = self.position + self.velocity
        self.position = np.minimum(self.position, [b[1] for b in bounds])
        self.position = np.maximum(self.position, [b[0] for b in bounds])