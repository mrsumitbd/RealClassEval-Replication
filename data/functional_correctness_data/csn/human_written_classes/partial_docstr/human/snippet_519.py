import scipy.sparse as sparse
import numpy as np

class BoundaryConditions:
    """
    Represents Dirichlet or Neumann boundary conditions for a PDE.
    """

    def __init__(self, shape):
        """
        Initializes the BoundaryCondition object.

        The BoundaryCondition objects needs information about the
        grid on which to solve the PDE, specifically the shape
        of the (equidistant) grid.

        Parameters
        ----------
        shape: tuple of ints
            the number of grid points in each dimension

        """
        self.shape = shape
        siz = np.prod(shape)
        self.long_indices = np.array(list(range(siz))).reshape(shape)
        self.lhs = sparse.lil_matrix((siz, siz))
        self.rhs = sparse.lil_matrix((siz, 1))

    def __setitem__(self, key, value):
        """
        Sets the boundary condition for specific grid points.

        Parameters
        ----------
        key: int, tuple of ints or slices
            where (on what grid points) to apply the boundary condition.
            Specified by the indices (or slices) of the grid point(s).

        value: Constant or FinDiff object
            the boundary condition to apply. Is a constant (scalar or array)
            for Dirichlet and a FinDiff object for Neumann boundary conditions
        """
        lng_inds = self.long_indices[key]
        if isinstance(value, tuple):
            op, value = value
            mat = sparse.lil_matrix(op.matrix(self.shape))
            self.lhs[lng_inds, :] = mat[lng_inds, :]
        else:
            self.lhs[lng_inds, lng_inds] = 1
        if isinstance(value, np.ndarray):
            value = value.reshape(-1)[lng_inds]
            for i, v in zip(lng_inds, value):
                self.rhs[i] = v
        else:
            self.rhs[lng_inds] = value

    def row_inds(self):
        nz_rows, nz_cols = self.lhs.nonzero()
        return nz_rows