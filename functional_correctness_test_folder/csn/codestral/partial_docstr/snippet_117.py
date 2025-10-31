
import numpy as np
from scipy.sparse import linalg


class PDE:

    def __init__(self, lhs, rhs, bcs):
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs

    def solve(self):
        A = self.lhs.matrix(self.bcs)
        b = self.rhs
        x = linalg.spsolve(A, b)
        return x
