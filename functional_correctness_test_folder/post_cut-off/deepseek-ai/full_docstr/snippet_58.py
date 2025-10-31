
import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        A = np.array(problem['matrix'])
        n = A.shape[0]
        L = np.eye(n)
        U = A.copy().astype(float)

        for i in range(n):
            if U[i, i] == 0:
                raise ValueError(
                    "Matrix is singular and cannot be factorized.")
            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, i:] -= factor * U[i, i:]

        return {'L': L.tolist(), 'U': U.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = np.array(problem['matrix'])
        L = np.array(solution['L'])
        U = np.array(solution['U'])

        reconstructed = np.dot(L, U)
        return np.allclose(A, reconstructed)
