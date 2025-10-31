import random


class Sampleable:
    def __init__(self):
        pass

    def get_sample(self):
        return random.random()

    def get_default_sample(self):
        return 0.5
