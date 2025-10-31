
class PDE:

    def __init__(self, lhs, rhs, bcs):
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs

    def solve(self):
        raise NotImplementedError(
            "The solve method must be implemented by subclasses.")
