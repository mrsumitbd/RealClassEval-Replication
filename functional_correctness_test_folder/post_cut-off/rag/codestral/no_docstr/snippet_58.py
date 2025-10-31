
import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.L = None
        self.U = None
        self.P = None

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        A = problem['matrix']
        P, L, U = self._lu_factorization(A)
        self.L = L
        self.U = U
        self.P = P
        return {'P': P, 'L': L, 'U': U}

    def _lu_factorization(self, A):
        '''
        Perform LU factorization with partial pivoting.
        Args:
            A: Input matrix
        Returns:
            P: Permutation matrix
            L: Lower triangular matrix
            U: Upper triangular matrix
        '''
        n = A.shape[0]
        P = np.eye(n)
        L = np.eye(n)
        U = A.copy().astype(float)

        for k in range(n-1):
            # Partial pivoting
            max_row = np.argmax(np.abs(U[k:, k])) + k
            if max_row != k:
                U[[k, max_row]] = U[[max_row, k]]
                P[[k, max_row]] = P[[max_row, k]]
                if k > 0:
                    L[[k, max_row], :k] = L[[max_row, k], :k]

            # Elimination
            for i in range(k+1, n):
                factor = U[i, k] / U[k, k]
                L[i, k] = factor
                U[i, k:] -= factor * U[k, k:]

        return P, L, U

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = problem['matrix']
        P = solution['P']
        L = solution['L']
        U = solution['U']

        # Check if PA = LU
        PA = np.dot(P, A)
        LU = np.dot(L, U)

        return np.allclose(PA, LU)
