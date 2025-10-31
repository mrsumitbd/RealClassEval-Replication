
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
        if hasattr(self.lhs, '__add__'):
            L = self.lhs.matrix(self.rhs.shape)
        else:
            L = self.lhs.matrix(self.rhs.shape)

        rhs_modified = self.rhs.copy()
        if hasattr(self.bcs, 'apply'):
            self.bcs.apply(L, rhs_modified)

        solution = np.linalg.solve(L, rhs_modified.flatten())
        return solution.reshape(self.rhs.shape)
