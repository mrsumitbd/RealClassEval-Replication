class BaseSolver:
    """Base class for all solvers."""

    def __init__(self):
        ...

    def solve(self):
        """Solves the given linear system of equations Ax=b."""
        raise NotImplementedError