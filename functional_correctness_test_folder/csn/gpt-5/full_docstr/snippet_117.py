import numpy as np

try:
    from scipy.sparse.linalg import spsolve
    from scipy.sparse import issparse
except Exception:  # pragma: no cover
    spsolve = None
    def issparse(x): return False


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
        if rhs is None:
            raise ValueError("rhs must be a numpy.ndarray")
        self.lhs = lhs
        self.rhs = np.asarray(rhs)
        self.bcs = bcs

    def _lhs_matrix(self, shape):
        lhs = self.lhs
        # Try common signatures used by FinDiff-like operators
        for attempt in (
            lambda: lhs.matrix(shape),
            lambda: lhs.matrix(shape=shape),
            lambda: lhs.tosparse(shape),  # some implementations
            lambda: lhs.tosparse(shape=shape),
            lambda: lhs.to_matrix(shape),
            lambda: lhs.to_matrix(shape=shape),
        ):
            try:
                A = attempt()
                if A is not None:
                    return A
            except TypeError:
                continue
            except AttributeError:
                continue
        # Fallback: try callable application to an identity basis (inefficient)
        # Only as a last resort if lhs is callable and shape is small.
        if callable(lhs):
            n = int(np.prod(shape))
            if n <= 10_000:
                eye = np.eye(n)
                try:
                    cols = []
                    for j in range(n):
                        e = eye[:, j].reshape(shape)
                        col = lhs(e).ravel()
                        cols.append(col)
                    A = np.column_stack(cols)
                    return A
                except Exception:
                    pass
        raise TypeError(
            "Could not build matrix from lhs; provide an operator with a 'matrix' method.")

    def _apply_bcs(self, A, b):
        if self.bcs is None:
            return A, b
        bcs = self.bcs
        # Try multiple conventions
        for attempt in (
            lambda: bcs.apply_to(A, b),
            lambda: bcs.apply(A, b),
            lambda: bcs(A, b),
        ):
            try:
                out = attempt()
                if isinstance(out, tuple) and len(out) == 2:
                    A2, b2 = out
                    return A2, b2
            except AttributeError:
                continue
            except TypeError:
                continue
        # Some APIs mutate in-place and return None
        for attempt in (
            lambda: bcs.apply_to(A, b),
            lambda: bcs.apply(A, b),
            lambda: bcs(A, b),
        ):
            try:
                res = attempt()
                if res is None:
                    return A, b
            except Exception:
                continue
        return A, b

    def solve(self):
        '''
        Solves the PDE.
        Returns
        -------
        out: numpy.ndarray
            Array with the solution of the PDE.
        '''
        shape = self.rhs.shape
        A = self._lhs_matrix(shape)
        b = np.asarray(self.rhs, dtype=float).ravel()

        A, b = self._apply_bcs(A, b)

        # Solve
        if spsolve is not None and issparse(A):
            x = spsolve(A, b)
        else:
            # Convert to ndarray if it's a sparse-like object without spsolve
            try:
                A_arr = A.toarray()
            except Exception:
                A_arr = np.asarray(A)
            x = np.linalg.solve(A_arr, b)

        return x.reshape(shape)
