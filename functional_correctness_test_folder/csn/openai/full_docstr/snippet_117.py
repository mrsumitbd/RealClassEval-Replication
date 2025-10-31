
import numpy as np


class PDE:
    '''
    Representation of a partial differential equation.
    '''

    def __init__(self, lhs, rhs, bcs):
        '''
        Initializes the PDE.
        You need to specify the left hand side (lhs) in terms of derivatives
        as well as the right hand side in terms of an array.
        Parameters
        ----------
        lhs: FinDiff object or combination of FinDiff objects
            the left hand side of the PDE
        rhs: numpy.ndarray
            the right hand side of the PDE
        bcs: BoundaryConditions
            the boundary conditions for the PDE
        '''
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs

    def solve(self):
        '''
        Solves the PDE.
        Returns
        -------
        out: numpy.ndarray
            Array with the solution of the PDE.
        '''
        # If the lhs object knows how to solve itself, delegate
        if hasattr(self.lhs, 'solve'):
            return self.lhs.solve(self.rhs, self.bcs)

        # Assemble the coefficient matrix A
        if isinstance(self.lhs, np.ndarray):
            A = self.lhs
        else:
            # Assume lhs is an iterable of matrices that can be summed
            try:
                A = sum(self.lhs)
            except TypeError:
                raise TypeError(
                    "lhs must be a numpy.ndarray or an iterable of matrices")

        # Apply boundary conditions if possible
        rhs = self.rhs
        if hasattr(self.bcs, 'apply'):
            A, rhs = self.bcs.apply(A, rhs)

        # Ensure rhs is a 1-D array
        rhs = np.asarray(rhs).reshape(-1)

        # Solve the linear system A * u = rhs
        try:
            solution = np.linalg.solve(A, rhs)
        except np.linalg.LinAlgError:
            # Fall back to least‑squares if A is singular or not square
            solution = np.linalg.lstsq(A, rhs, rcond=None)[0]

        return solution
