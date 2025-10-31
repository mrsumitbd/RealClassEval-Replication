from numpy import ndarray
from typing import List

class PerturbationProblem:

    def __init__(self, f: List[ndarray], g: List[ndarray], sigma: ndarray):
        self.f = f
        self.g = g
        self.sigma = sigma
        assert len(f) == len(g)

    @property
    def order(self):
        return len(self.f) - 1