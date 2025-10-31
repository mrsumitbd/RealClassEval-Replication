
import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        A = problem['A']
        n = A.shape[0]
        LU = np.copy(A)
        P = np.eye(n)

        for i in range(n-1):
            # Partial pivoting
            max_idx = np.argmax(np.abs(LU[i:, i])) + i
            if max_idx != i:
                # Swap rows in LU
                LU[[i, max_idx]] = LU[[max_idx, i]]
                # Swap rows in P
                P[[i, max_idx]] = P[[max_idx, i]]

            # Check for singularity
            if LU[i, i] == 0:
                raise ValueError("Matrix is singular")

            # Perform Gaussian elimination
            LU[i+1:, i] /= LU[i, i]
            LU[i+1:, i+1:] -= np.outer(LU[i+1:, i], LU[i, i+1:])

        L = np.tril(LU, -1) + np.eye(n)
        U = np.triu(LU)

        return {'LU': LU, 'P': P, 'L': L, 'U': U}

    def is_solution(self, problem, solution):
        A = problem['A']
        LU = solution.get('LU')
        P = solution.get('P')
        L = solution.get('L')
        U = solution.get('U')

        # Check presence of 'LU' with 'P','L','U'
        if not all([LU is not None, P is not None, L is not None, U is not None]):
            return False

        # Check shapes match A (square)
        n = A.shape[0]
        if not (LU.shape == (n, n) and P.shape == (n, n) and L.shape == (n, n) and U.shape == (n, n)):
            return False

        # Check for NaNs/Infs
        if np.any(np.isnan(LU)) or np.any(np.isinf(LU)) or np.any(np.isnan(P)) or np.any(np.isinf(P)) or np.any(np.isnan(L)) or np.any(np.isinf(L)) or np.any(np.isnan(U)) or np.any(np.isinf(U)):
            return False

        # Check P is a permutation matrix
        if not (np.allclose(np.dot(P.T, P), np.eye(n)) and np.allclose(np.dot(P, P.T), np.eye(n))):
            return False

        # Check L is lower-triangular
        if not np.allclose(L, np.tril(L)):
            return False

        # Check U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check P @ L @ U ≈ A
        if not np.allclose(np.dot(P, np.dot(L, U)), A):
            return False

        return True
