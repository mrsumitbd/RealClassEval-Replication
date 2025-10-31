
import numpy as np
from scipy.sparse.linalg import spsolve


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
        self.lhs_matrix = self.lhs.matrix(shape=rhs.shape)

    def solve(self):
        '''
        Solves the PDE.
        Returns
        -------
        out: numpy.ndarray
            Array with the solution of the PDE.
        '''
        # Apply boundary conditions to the matrix and rhs
        lhs_matrix = self.bcs.apply(self.lhs_matrix)
        rhs = self.bcs.apply_to_rhs(self.rhs)

        # Solve the linear system
        solution = spsolve(lhs_matrix, rhs.ravel())

        # Reshape the solution to the original shape
        solution = solution.reshape(self.rhs.shape)

        return solution
