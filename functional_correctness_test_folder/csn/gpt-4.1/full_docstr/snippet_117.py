
import numpy as np
from scipy.sparse import csr_matrix, identity
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

    def solve(self):
        '''
        Solves the PDE.
        Returns
        -------
        out: numpy.ndarray
            Array with the solution of the PDE.
        '''
        # Assume lhs is a FinDiff object or sum of FinDiff objects
        # and has a 'matrix' method that returns a sparse matrix operator
        # Assume bcs has an 'apply' method that modifies the matrix and rhs

        # Get the shape of the problem
        shape = self.rhs.shape
        size = np.prod(shape)

        # Build the operator matrix
        if hasattr(self.lhs, 'matrix'):
            A = self.lhs.matrix(shape)
        else:
            # Assume lhs is a sum of FinDiff objects
            A = sum(term.matrix(shape) for term in self.lhs)

        # Flatten the rhs
        b = self.rhs.flatten()

        # Apply boundary conditions
        if hasattr(self.bcs, 'apply'):
            A, b = self.bcs.apply(A, b, shape)
        else:
            # If no apply method, assume no modification
            pass

        # Solve the linear system
        x = spsolve(A, b)

        # Reshape to original shape
        return x.reshape(shape)
