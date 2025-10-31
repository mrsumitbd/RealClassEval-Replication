
import numpy as np
from scipy.sparse import linalg


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
        A = self.lhs.matrix(self.bcs.domain)
        b = self.rhs
        self.bcs.apply(A, b)
        solution = linalg.spsolve(A, b)
        return solution
