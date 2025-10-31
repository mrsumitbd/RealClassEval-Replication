class PDE:

    def __init__(self, lhs, rhs, bcs):
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs
        self.n = 100
        self.domain = (0.0, 1.0)

    def _thomas_tridiagonal(self, a, b, c, d):
        n = len(d)
        cp = c.copy()
        bp = b.copy()
        dp = d.copy()

        for i in range(1, n):
            m = a[i - 1] / bp[i - 1]
            bp[i] = bp[i] - m * cp[i - 1]
            dp[i] = dp[i] - m * dp[i - 1]

        x = dp
        x[-1] = dp[-1] / bp[-1]
        for i in range(n - 2, -1, -1):
            x[i] = (dp[i] - cp[i] * x[i + 1]) / bp[i]
        return x

    def solve(self):
        import numpy as np

        # Case 1: user provides a full discrete operator matrix
        if hasattr(self.lhs, "shape") and len(getattr(self.lhs, "shape", ())) == 2:
            A = np.asarray(self.lhs, dtype=float)
            b = self.rhs
            if callable(b):
                raise ValueError(
                    "rhs cannot be callable when lhs is a matrix.")
            b = np.asarray(b, dtype=float)
            if A.shape[0] != A.shape[1] or A.shape[0] != b.shape[0]:
                raise ValueError(
                    "Incompatible shapes between lhs matrix and rhs vector.")
            u = np.linalg.solve(A, b)
            return u

        # Case 2: user provides a callable to construct the discrete operator
        if callable(self.lhs):
            A_x = self.lhs
            a, bdom = self.domain
            A, x = A_x(self.n, a, bdom)
            bvec = self.rhs
            if callable(bvec):
                bvec = np.asarray([bvec(xi) for xi in x], dtype=float)
            else:
                bvec = np.asarray(bvec, dtype=float)
                if bvec.shape[0] != A.shape[0]:
                    raise ValueError(
                        "rhs length does not match operator size.")
            u = np.linalg.solve(A, bvec)
            return u

        # Default: 1D Poisson problem on [a,b] with Dirichlet BCs
        if not isinstance(self.bcs, (tuple, list)) or len(self.bcs) != 2:
            raise ValueError(
                "For default 1D Poisson solver, bcs must be a tuple (u_a, u_b).")
        ua, ub = float(self.bcs[0]), float(self.bcs[1])

        a, bdom = self.domain
        n = int(self.n)
        if n < 1:
            raise ValueError("n must be >= 1.")
        h = (bdom - a) / (n + 1)
        x_interior = np.linspace(a + h, bdom - h, n)

        if callable(self.rhs):
            f = np.asarray([self.rhs(xi) for xi in x_interior], dtype=float)
        else:
            f = np.asarray(self.rhs, dtype=float)
            if f.shape[0] != n:
                raise ValueError(
                    "rhs length must match the number of interior points.")
        d = (h * h) * f
        if n >= 1:
            d[0] += ua
            d[-1] += ub

        lower = -np.ones(n - 1)
        main = 2.0 * np.ones(n)
        upper = -np.ones(n - 1)

        u_interior = self._thomas_tridiagonal(lower, main, upper, d)
        x_all = np.concatenate(([a], x_interior, [bdom]))
        u_all = np.concatenate(([ua], u_interior, [ub]))
        return x_all, u_all
