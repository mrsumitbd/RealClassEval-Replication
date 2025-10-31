import numpy as np


class LUFactorization:

    def __init__(self, tol=1e-9, rtol=1e-7, atol=1e-9, return_factors=False):
        self.tol = tol
        self.rtol = rtol
        self.atol = atol
        self.return_factors = return_factors

    def solve(self, problem):
        A, b = self._parse_problem(problem)
        L, U, piv = self._lu_factor(A)
        x = self._lu_solve(L, U, piv, b)
        if self.return_factors:
            return {"x": x, "L": L, "U": U, "piv": piv}
        return x

    def is_solution(self, problem, solution):
        A, b = self._parse_problem(problem)
        x = self._parse_solution(solution)
        if x is None:
            return False
        if x.ndim == 1:
            res = A @ x - b
            return self._check_residual(res, A, x, b)
        else:
            # Multiple RHS
            res = A @ x - b
            if res.ndim == 1:
                res = res[:, None]
            checks = [self._check_residual(
                res[:, i], A, x[:, i], b[:, i] if b.ndim > 1 else b) for i in range(res.shape[1])]
            return all(checks)

    def _parse_problem(self, problem):
        if isinstance(problem, dict):
            A = problem.get("A", None)
            b = problem.get("b", None)
        elif isinstance(problem, (list, tuple)) and len(problem) == 2:
            A, b = problem
        else:
            raise ValueError(
                "Problem must be a dict with keys 'A' and 'b' or a tuple/list (A, b).")
        if A is None or b is None:
            raise ValueError("Problem missing 'A' or 'b'.")
        A = np.array(A, dtype=float, copy=True)
        b = np.array(b, dtype=float, copy=True)
        if A.ndim != 2:
            raise ValueError("A must be a 2D array.")
        n, m = A.shape
        if n != m:
            raise ValueError("A must be square.")
        if b.ndim == 1:
            if b.shape[0] != n:
                raise ValueError("b length must match A dimension.")
        elif b.ndim == 2:
            if b.shape[0] != n:
                raise ValueError("b row count must match A dimension.")
        else:
            raise ValueError("b must be 1D or 2D.")
        return A, b

    def _parse_solution(self, solution):
        if isinstance(solution, dict):
            if "x" in solution:
                x = np.array(solution["x"], dtype=float, copy=False)
            else:
                # If dict contains factors, attempt to derive x if possible (not enough info)
                return None
        else:
            x = np.array(solution, dtype=float, copy=False)
        if x.ndim not in (1, 2):
            return None
        return x

    def _check_residual(self, r, A, x, b):
        abs_ok = np.linalg.norm(r, ord=np.inf) <= self.atol
        denom = np.linalg.norm(A, ord=np.inf) * np.linalg.norm(x,
                                                               ord=np.inf) + np.linalg.norm(b, ord=np.inf) + 1e-16
        rel_ok = np.linalg.norm(r, ord=np.inf) <= self.rtol * denom
        return bool(abs_ok or rel_ok)

    def _lu_factor(self, A):
        A = np.array(A, dtype=float, copy=True)
        n = A.shape[0]
        piv = np.arange(n)
        for k in range(n):
            # Pivot selection
            pivot_row = k + np.argmax(np.abs(A[k:, k]))
            if np.abs(A[pivot_row, k]) <= self.tol:
                raise np.linalg.LinAlgError(
                    "Matrix is singular to working precision.")
            if pivot_row != k:
                A[[k, pivot_row], :] = A[[pivot_row, k], :]
                piv[[k, pivot_row]] = piv[[pivot_row, k]]
            # Elimination
            if k < n - 1:
                A[k+1:, k] /= A[k, k]
                A[k+1:, k+1:] -= np.outer(A[k+1:, k], A[k, k+1:])
        L = np.tril(A, k=-1) + np.eye(n, dtype=A.dtype)
        U = np.triu(A)
        return L, U, piv

    def _lu_solve(self, L, U, piv, b):
        n = L.shape[0]
        if b.ndim == 1:
            bp = b[piv]
            y = self._forward_substitution(L, bp)
            x = self._back_substitution(U, y)
            return x
        else:
            # multiple RHS
            bp = b[piv, :]
            y = np.column_stack([self._forward_substitution(
                L, bp[:, i]) for i in range(bp.shape[1])])
            x = np.column_stack([self._back_substitution(U, y[:, i])
                                for i in range(y.shape[1])])
            return x

    def _forward_substitution(self, L, b):
        n = L.shape[0]
        y = np.empty_like(b, dtype=float)
        for i in range(n):
            s = np.dot(L[i, :i], y[:i]) if i > 0 else 0.0
            y[i] = (b[i] - s)  # L has unit diagonal
        return y

    def _back_substitution(self, U, y):
        n = U.shape[0]
        x = np.empty_like(y, dtype=float)
        for i in range(n - 1, -1, -1):
            s = np.dot(U[i, i+1:], x[i+1:]) if i < n - 1 else 0.0
            if np.abs(U[i, i]) <= self.tol:
                raise np.linalg.LinAlgError(
                    "Matrix is singular to working precision.")
            x[i] = (y[i] - s) / U[i, i]
        return x
