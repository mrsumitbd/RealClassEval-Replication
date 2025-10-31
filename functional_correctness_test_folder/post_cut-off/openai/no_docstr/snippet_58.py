
import numpy as np


class LUFactorization:
    def __init__(self):
        # No pre‑computed data needed
        pass

    def _lu_decompose(self, A):
        """
        Perform LU decomposition with partial pivoting.
        Returns L, U, and the permutation matrix P such that P @ A = L @ U.
        """
        n = A.shape[0]
        U = A.copy().astype(float)
        L = np.eye(n, dtype=float)
        P = np.eye(n, dtype=float)

        for k in range(n):
            # Partial pivoting
            pivot = np.argmax(np.abs(U[k:, k])) + k
            if U[pivot, k] == 0:
                raise ValueError("Matrix is singular.")
            if pivot != k:
                # Swap rows in U
                U[[k, pivot], :] = U[[pivot, k], :]
                # Swap rows in P
                P[[k, pivot], :] = P[[pivot, k], :]
                if k > 0:
                    # Swap the lower part of L
                    L[[k, pivot], :k] = L[[pivot, k], :k]

            # Compute multipliers and eliminate
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] -= L[i, k] * U[k, k:]

        return L, U, P

    def _forward_substitution(self, L, b):
        """Solve L y = b for y (L is lower triangular with unit diagonal)."""
        n = L.shape[0]
        y = np.zeros_like(b, dtype=float)
        for i in range(n):
            y[i] = b[i] - L[i, :i] @ y[:i]
        return y

    def _back_substitution(self, U, y):
        """Solve U x = y for x (U is upper triangular)."""
        n = U.shape[0]
        x = np.zeros_like(y, dtype=float)
        for i in range(n - 1, -1, -1):
            if U[i, i] == 0:
                raise ValueError("Matrix is singular.")
            x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
        return x

    def solve(self, problem):
        """
        Solve a linear system A x = b.
        `problem` can be a tuple/list (A, b) or an object with attributes `A` and `b`.
        Returns the solution vector x.
        """
        if isinstance(problem, (tuple, list)):
            A, b = problem
        else:
            A = getattr(problem, "A")
            b = getattr(problem, "b")

        A = np.asarray(A, dtype=float)
        b = np.asarray(b, dtype=float)

        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix A must be square.")
        if b.ndim != 1 or b.shape[0] != A.shape[0]:
            raise ValueError("Vector b must have compatible dimensions.")

        L, U, P = self._lu_decompose(A)
        # Apply permutation to b
        Pb = P @ b
        y = self._forward_substitution(L, Pb)
        x = self._back_substitution(U, y)
        return x

    def is_solution(self, problem, solution, tol=1e-8):
        """
        Check whether `solution` satisfies the linear system within a tolerance.
        Returns True if ||A x - b||_inf <= tol, else False.
        """
        if isinstance(problem, (tuple, list)):
            A, b = problem
        else:
            A = getattr(problem, "A")
            b = getattr(problem, "b")

        A = np.asarray(A, dtype=float)
        b = np.asarray(b, dtype=float)
        x = np.asarray(solution, dtype=float)

        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix A must be square.")
        if b.ndim != 1 or b.shape[0] != A.shape[0]:
            raise ValueError("Vector b must have compatible dimensions.")
        if x.ndim != 1 or x.shape[0] != A.shape[1]:
            raise ValueError("Solution vector has incompatible dimensions.")

        residual = A @ x - b
        return np.linalg.norm(residual, ord=np.inf) <= tol
