
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
        A = problem.get('matrix')
        if A is None:
            raise ValueError(
                "Problem must contain a 'matrix' key with a numpy array.")

        A = np.array(A, dtype=float)
        n = A.shape[0]

        # Initialize L and U
        L = np.eye(n, dtype=float)
        U = np.zeros((n, n), dtype=float)
        P = np.eye(n, dtype=float)

        for k in range(n):
            # Partial pivoting
            max_row = np.argmax(np.abs(A[k:, k])) + k
            if max_row != k:
                A[[k, max_row]] = A[[max_row, k]]
                P[[k, max_row]] = P[[max_row, k]]

            # LU decomposition
            for i in range(k, n):
                U[k, i] = A[k, i]
                L[i, k] = A[i, k] / U[k, k]

            for i in range(k + 1, n):
                for j in range(k + 1, n):
                    A[i, j] = A[i, j] - L[i, k] * U[k, j]

        self.L = L
        self.U = U
        self.P = P

        return {
            'L': L.tolist(),
            'U': U.tolist(),
            'P': P.tolist()
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = np.array(problem.get('matrix'), dtype=float)
        L = np.array(solution.get('L'), dtype=float)
        U = np.array(solution.get('U'), dtype=float)
        P = np.array(solution.get('P'), dtype=float)

        # Check if PA = LU
        PA = np.dot(P, A)
        LU = np.dot(L, U)

        return np.allclose(PA, LU)
