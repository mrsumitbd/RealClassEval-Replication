
import numpy as np
from scipy.sparse import csr_matrix, identity
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

    def solve(self):
        # Assume lhs is a FinDiff object or sum of FinDiff objects
        # and has a matrix() method that returns the sparse matrix operator
        # bcs is a BoundaryConditions object with apply(A, b) method
        # rhs is a numpy array

        # Get the operator matrix
        A = self.lhs.matrix(self.rhs.shape)
        b = self.rhs.copy()

        # Apply boundary conditions
        A_bc, b_bc = self.bcs.apply(A, b)

        # Solve the linear system
        x = spsolve(A_bc, b_bc)
        return x.reshape(self.rhs.shape)
