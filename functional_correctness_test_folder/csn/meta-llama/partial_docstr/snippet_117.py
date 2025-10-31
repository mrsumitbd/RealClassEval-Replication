
import numpy as np
from scipy.sparse.linalg import spsolve


class PDE:

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
        self.bcs.apply(self.lhs_matrix, self.rhs)

    def solve(self):
        return spsolve(self.lhs_matrix, self.rhs)
