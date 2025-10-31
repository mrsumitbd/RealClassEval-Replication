
import random


class Reservoir:

    def __init__(self, traces_per_sec=0):
        self.traces_per_sec = traces_per_sec
        self.sample_size = 0
        self.sample = []

    def take(self):
        if self.traces_per_sec == 0:
            return False

        self.sample_size += 1
        if len(self.sample) < self.traces_per_sec:
            self.sample.append(1)
            return True

        rand_idx = random.randint(0, self.sample_size - 1)
        if rand_idx < self.traces_per_sec:
            self.sample[rand_idx] = 1
            return True

        return False
