import numpy as np
from scipy.sparse.linalg import spsolve
import scipy.sparse as sparse

class PDE:
    """
    Representation of a partial differential equation.
    """

    def __init__(self, lhs, rhs, bcs):
        """
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

        """
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs
        self._L = None

    def solve(self):
        """
        Solves the PDE.

        Returns
        -------
        out: numpy.ndarray
            Array with the solution of the PDE.
        """
        shape = self.bcs.shape
        if self._L is None:
            self._L = self.lhs.matrix(shape)
        L = sparse.lil_matrix(self._L)
        f = self.rhs.reshape(-1, 1)
        nz = list(self.bcs.row_inds())
        L[nz, :] = self.bcs.lhs[nz, :]
        f[nz] = np.array(self.bcs.rhs[nz].toarray()).reshape(-1, 1)
        L = sparse.csr_matrix(L)
        return spsolve(L, f).reshape(shape)