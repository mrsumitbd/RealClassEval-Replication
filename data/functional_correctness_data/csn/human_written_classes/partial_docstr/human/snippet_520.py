from sympy import Add, IndexedBase, Matrix, Rational, Symbol, factorial, linsolve

class SymbolicDiff:
    """
    A symbolic representation of the finite difference approximation
    of a partial derivative. Based on *sympy*.
    """

    def __init__(self, mesh, axis=0, degree=1):
        """Constructor

        Parameters
        ----------
        mesh: SymbolicMesh
            The symbolic grid on which to evaluate the derivative.
        axis: int
            The index of the axis with respect to which to differentiate.
        degree: int > 0
            The degree of the partial derivative.

        """
        self.mesh = mesh
        self.axis = axis
        self.degree = degree

    def __call__(self, f, at, offsets):
        if not isinstance(at, tuple) and (not isinstance(at, list)):
            at = [at]
        if self.mesh.ndims != len(at):
            raise ValueError('Index tuple must match the number of dimensions!')
        coefs = self._compute_coefficients(f, at, offsets)
        terms = []
        for coef, off in zip(coefs, offsets):
            inds = list(at)
            inds[self.axis] += off
            inds = tuple(inds)
            terms.append(coef * f[inds])
        return Add(*terms).simplify()

    def _compute_coefficients(self, f, at, offsets):
        n = len(offsets)
        matrix = [[1] * n]

        def spac(off):
            """A helper function to get the spacing between grid points."""
            if self.mesh.equidistant:
                h = self.mesh.spacing[self.axis]
            else:
                x = self.mesh.coord[self.axis]
                h = x[at[self.axis] + off] - x[at[self.axis]]
            return h
        for i in range(1, n):
            ifac = Rational(1, factorial(i))
            row = [ifac * (off * spac(off)) ** i for off in offsets]
            matrix.append(row)
        rhs = [0] * n
        rhs[self.degree] = 1
        matrix = Matrix(matrix)
        rhs = Matrix(rhs)
        sol = linsolve((matrix, rhs))
        return list(sol)[0].simplify()