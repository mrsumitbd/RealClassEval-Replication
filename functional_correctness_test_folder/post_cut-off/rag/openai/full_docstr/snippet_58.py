
import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        # No state needed for this simple implementation
        pass

    def _lu_decompose(self, A):
        """
        Perform LU decomposition with partial pivoting.
        Returns L, U, P such that P @ A = L @ U.
        """
        A = np.array(A, dtype=float)
        n = A.shape[0]
        if A.shape[0] != A.shape[1]:
            raise ValueError("Matrix A must be square for LU decomposition.")
        L = np.eye(n, dtype=float)
        U = A.copy()
        P = np.eye(n, dtype=float)

        for k in range(n):
            # Partial pivoting
            pivot = np.argmax(np.abs(U[k:, k])) + k
            if U[pivot, k] == 0:
                raise np.linalg.LinAlgError("Matrix is singular.")
            if pivot != k:
                # Swap rows in U
                U[[k, pivot], :] = U[[pivot, k], :]
                # Swap rows in P
                P[[k, pivot], :] = P[[pivot, k], :]
                if k > 0:
                    # Swap rows in L for columns < k
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
            y[i] = b[i] - np.dot(L[i, :i], y[:i])
        return y

    def _backward_substitution(self, U, y):
        """Solve U x = y for x (U is upper triangular)."""
        n = U.shape[0]
        x = np.zeros_like(y, dtype=float)
        for i in range(n - 1, -1, -1):
            if U[i, i] == 0:
                raise np.linalg.LinAlgError("Matrix is singular.")
            x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]
        return x

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
                     Expected keys:
                         'A' : 2D array-like, square coefficient matrix
                         'b' : 1D or 2D array-like, right-hand side vector/matrix
        Returns:
            The solution vector x (1D numpy array) or matrix X (2D numpy array)
        '''
        A = problem.get('A')
        b = problem.get('b')
        if A is None or b is None:
            raise ValueError(
                "Problem dictionary must contain 'A' and 'b' keys.")
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)

        # Ensure b is a column vector if 1D
        if b.ndim == 1:
            b = b.reshape(-1, 1)

        L, U, P = self._lu_decompose(A)
        # Apply permutation to b
        Pb = P @ b
        y = self._forward_substitution(L, Pb)
        x = self._backward_substitution(U, y)

        # Return as 1D array if original b was 1D
        if x.shape[1] == 1:
            return x.ravel()
        return x

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = problem.get('A')
        b = problem.get('b')
        if A is None or b is None:
            raise ValueError(
                "Problem dictionary must contain 'A' and 'b' keys.")
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        solution = np.array(solution, dtype=float)

        # Compute residual
        residual = A @ solution - b
        # Use relative tolerance
        norm_residual = np.linalg.norm(residual)
        norm_b = np.linalg.norm(b)
        tol = 1e-8
        return norm_residual <= tol * max(1.0, norm_b)
