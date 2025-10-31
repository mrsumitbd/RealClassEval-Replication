
import numpy as np


class LUFactorization:
    def __init__(self):
        # No pre‑allocation needed for this simple implementation
        pass

    def solve(self, problem):
        """
        Solve the linear system A x = b using LU factorization.

        Parameters
        ----------
        problem : dict
            Must contain:
                - 'A' : 2‑D array‑like, square matrix
                - 'b' : 1‑D array‑like, right‑hand side vector

        Returns
        -------
        x : ndarray
            Solution vector.
        """
        A = np.asarray(problem['A'], dtype=float)
        b = np.asarray(problem['b'], dtype=float)

        # Basic LU factorization with partial pivoting
        n = A.shape[0]
        LU = A.copy()
        piv = np.arange(n)

        for k in range(n):
            # Pivot selection
            max_row = np.argmax(np.abs(LU[k:, k])) + k
            if LU[max_row, k] == 0:
                raise ValueError("Matrix is singular.")
            if max_row != k:
                LU[[k, max_row], :] = LU[[max_row, k], :]
                piv[[k, max_row]] = piv[[max_row, k]]

            # Elimination
            for i in range(k + 1, n):
                LU[i, k] /= LU[k, k]
                LU[i, k + 1:] -= LU[i, k] * LU[k, k + 1:]

        # Forward substitution Ly = Pb
        y = np.empty(n, dtype=float)
        for i in range(n):
            y[i] = b[piv[i]] - np.dot(LU[i, :i], y[:i])

        # Backward substitution Ux = y
        x = np.empty(n, dtype=float)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(LU[i, i + 1:], x[i + 1:])) / LU[i, i]

        return x

    def is_solution(self, problem, solution, atol=1e-8, rtol=1e-5):
        """
        Verify that the provided solution satisfies A x = b within tolerances.

        Parameters
        ----------
        problem : dict
            Must contain 'A' and 'b'.
        solution : array‑like
            Candidate solution vector.
        atol : float
            Absolute tolerance.
        rtol : float
            Relative tolerance.

        Returns
        -------
        bool
            True if the solution is acceptable, False otherwise.
        """
        A = np.asarray(problem['A'], dtype=float)
        b = np.asarray(problem['b'], dtype=float)
        x = np.asarray(solution, dtype=float)

        residual = A @ x - b
        return np.allclose(residual, np.zeros_like(b), atol=atol, rtol=rtol)
