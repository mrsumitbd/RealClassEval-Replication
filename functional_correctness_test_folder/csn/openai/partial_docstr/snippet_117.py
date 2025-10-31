
import numpy as np


class PDE:
    """
    A simple PDE solver that accepts a left‑hand side (lhs) represented by a FinDiff
    object (or a combination of such objects), a right‑hand side array (rhs), and
    boundary conditions (bcs). The solver assembles the linear system, applies
    the boundary conditions, and solves for the unknown field.
    """

    def __init__(self, lhs, rhs, bcs):
        """
        Initializes the PDE.

        Parameters
        ----------
        lhs : FinDiff or combination of FinDiff objects
            The left hand side of the PDE. It must provide a method `to_matrix`
            that returns the discretised matrix representation.
        rhs : numpy.ndarray
            The right hand side of the PDE. Must be a 1‑D array of the same
            length as the number of unknowns in `lhs`.
        bcs : BoundaryConditions
            The boundary conditions for the PDE. It must provide a method
            `apply` that takes a matrix and a vector and returns the modified
            matrix and vector.
        """
        # Basic type checks
        if not hasattr(lhs, "to_matrix"):
            raise TypeError("lhs must provide a `to_matrix` method.")
        if not isinstance(rhs, np.ndarray):
            raise TypeError("rhs must be a numpy.ndarray.")
        if not hasattr(bcs, "apply"):
            raise TypeError("bcs must provide an `apply` method.")

        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs

    def solve(self):
        """
        Assembles the linear system, applies boundary conditions, and solves
        for the unknown field.

        Returns
        -------
        solution : numpy.ndarray
            The solution vector.
        """
        # Assemble the matrix and RHS vector from the FinDiff object
        A = self.lhs.to_matrix()
        b = self.rhs.copy()

        # Apply boundary conditions
        A, b = self.bcs.apply(A, b)

        # Solve the linear system
        try:
            solution = np.linalg.solve(A, b)
        except np.linalg.LinAlgError as exc:
            raise RuntimeError("Linear system could not be solved.") from exc

        return solution
