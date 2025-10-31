
import numpy as np


class LUFactorization:
    def __init__(self):
        pass

    def solve(self, problem):
        """
        Compute the LU factorization with partial pivoting for the matrix
        stored under the key 'A' in the problem dictionary.

        Parameters
        ----------
        problem : dict
            Must contain a key 'A' with a 2‑D square numpy array.

        Returns
        -------
        dict
            Dictionary containing the factorization under the key 'LU':
            {
                'LU': {
                    'P': P,
                    'L': L,
                    'U': U
                }
            }
        """
        if 'A' not in problem:
            raise KeyError("Problem dictionary must contain key 'A'")
        A = np.asarray(problem['A'], dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'A' must be a square matrix")

        n = A.shape[0]
        P = np.eye(n, dtype=float)
        L = np.zeros((n, n), dtype=float)
        U = A.copy()

        for k in range(n):
            # Partial pivoting
            pivot = np.argmax(np.abs(U[k:, k])) + k
            if np.isclose(U[pivot, k], 0.0):
                raise np.linalg.LinAlgError("Matrix is singular")

            if pivot != k:
                # Swap rows in U
                U[[k, pivot], :] = U[[pivot, k], :]
                # Swap rows in P
                P[[k, pivot], :] = P[[pivot, k], :]
                # Swap rows in L for columns < k
                if k > 0:
                    L[[k, pivot], :k] = L[[pivot, k], :k]

            # Set diagonal of L to 1
            L[k, k] = 1.0

            # Compute multipliers and eliminate below pivot
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, :] -= L[i, k] * U[k, :]

        return {'LU': {'P': P, 'L': L, 'U': U}}

    def is_solution(self, problem, solution):
        """
        Validate an LU factorization A = P L U.

        Parameters
        ----------
        problem : dict
            Must contain key 'A' with the original matrix.
        solution : dict
            Must contain key 'LU' with subkeys 'P', 'L', 'U'.

        Returns
        -------
        bool
            True if the factorization is valid, False otherwise.
        """
        # Check presence of required keys
        if 'A' not in problem:
            return False
        if 'LU' not in solution:
            return False
        lu = solution['LU']
        if not all(k in lu for k in ('P', 'L', 'U')):
            return False

        A = np.asarray(problem['A'], dtype=float)
        P = np.asarray(lu['P'], dtype=float)
        L = np.asarray(lu['L'], dtype=float)
        U = np.asarray(lu['U'], dtype=float)

        # Shape checks
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        n = A.shape[0]
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # Finite values check
        if not (np.isfinite(A).all() and np.isfinite(P).all()
                and np.isfinite(L).all() and np.isfinite(U).all()):
            return False

        # P is a permutation matrix: each row and column has exactly one 1
        if not (np.allclose(P, np.round(P)) and
                np.allclose(P @ P.T, np.eye(n))):
            return False

        # L lower triangular with unit diagonal
        if not np.allclose(L, np.tril(L)):
            return False
        if not np.allclose(np.diag(L), np.ones(n)):
            return False

        # U upper triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Reconstruct A and compare
        reconstructed = P @ L @ U
        if not np.allclose(reconstructed, A, atol=1e-8, rtol=1e-8):
            return False

        return True
