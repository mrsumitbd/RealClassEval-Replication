
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
        matrix = problem['matrix']
        n = len(matrix)
        L = np.zeros((n, n))
        U = np.zeros((n, n))

        for i in range(n):
            L[i][i] = 1.0

            for j in range(i, n):
                sum_u = sum(L[i][k] * U[k][j] for k in range(i))
                U[i][j] = matrix[i][j] - sum_u

            for j in range(i + 1, n):
                sum_l = sum(L[j][k] * U[k][i] for k in range(i))
                L[j][i] = (matrix[j][i] - sum_l) / U[i][i]

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
        matrix = np.array(problem['matrix'])
        L = np.array(solution['L'])
        U = np.array(solution['U'])
        reconstructed = np.dot(L, U)
        return np.allclose(matrix, reconstructed)
