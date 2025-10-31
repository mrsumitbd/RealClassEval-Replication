import numpy as np

try:
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla
except Exception:  # allow operation without scipy at import time
    sp = None
    spla = None


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
        self.rhs = np.asarray(rhs)
        self.shape = self.rhs.shape
        self.size = int(np.prod(self.shape)) if self.shape else 1
        self.bcs = bcs
        self.A = None
        self.b = None
        self.u = None

    def _build_matrix(self):
        lhs = self.lhs
        shape = self.shape

        # Try common APIs to obtain a system matrix
        A = None
        # scipy sparse preferred if available
        if hasattr(lhs, "sparse_matrix"):
            try:
                A = lhs.sparse_matrix(shape)
            except TypeError:
                # some implementations expect unpacked shape
                A = lhs.sparse_matrix(*shape)
        elif hasattr(lhs, "matrix"):
            try:
                A = lhs.matrix(shape)
            except TypeError:
                A = lhs.matrix(*shape)
        elif hasattr(lhs, "to_matrix"):
            try:
                A = lhs.to_matrix(shape)
            except TypeError:
                A = lhs.to_matrix(*shape)

        if A is None:
            raise TypeError(
                "Cannot build system matrix from lhs; expected an object with sparse_matrix/matrix/to_matrix methods")

        # Normalize matrix type
        if sp is not None and sp.issparse(A):
            A = A.tocsr()
        else:
            A = np.array(A)

        return A

    def _apply_bcs(self, A, b):
        bcs = self.bcs
        if bcs is None:
            return A, b

        # Support different styles of boundary condition applicators
        # Expected to return possibly modified (A, b)
        if hasattr(bcs, "apply"):
            try:
                out = bcs.apply(A, b, rhs_shape=self.shape)
            except TypeError:
                out = bcs.apply(A, b)
        elif hasattr(bcs, "apply_to"):
            out = bcs.apply_to(A, b)
        elif isinstance(bcs, (list, tuple)):
            outA, outb = A, b
            for bc in bcs:
                if hasattr(bc, "apply"):
                    try:
                        outA, outb = bc.apply(outA, outb, rhs_shape=self.shape)
                    except TypeError:
                        outA, outb = bc.apply(outA, outb)
                elif hasattr(bc, "apply_to"):
                    outA, outb = bc.apply_to(outA, outb)
                else:
                    raise TypeError(
                        "Boundary condition element does not provide apply/apply_to")
            out = (outA, outb)
        else:
            raise TypeError(
                "Unsupported BoundaryConditions object; expected apply/apply_to or list of such")

        if not isinstance(out, tuple) or len(out) != 2:
            raise ValueError(
                "BoundaryConditions.apply/apply_to must return (A, b)")
        return out

    def _solve_linear_system(self, A, b):
        # Prefer sparse solvers when possible
        if sp is not None and sp.issparse(A):
            if spla is None:
                raise ImportError("scipy is required to solve sparse systems")
            return spla.spsolve(A, b)
        # Support LinearOperator (iterative)
        if spla is not None and isinstance(A, spla.LinearOperator):
            x, info = spla.gmres(A, b)
            if info != 0:
                raise RuntimeError(
                    f"Iterative solver did not converge, info={info}")
            return x
        # Dense solve
        return np.linalg.solve(np.asarray(A), b)

    def solve(self):
        A = self._build_matrix()
        b = np.asarray(self.rhs, dtype=float).reshape(-1)

        A, b = self._apply_bcs(A, b)

        x = self._solve_linear_system(A, b)

        self.A = A
        self.b = b
        self.u = x.reshape(self.shape)
        return self.u
