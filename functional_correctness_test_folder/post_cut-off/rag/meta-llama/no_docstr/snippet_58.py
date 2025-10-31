
import numpy as np
from scipy.linalg import lu_factor, lu_solve


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
        matrix = np.array(problem['matrix'])
        lu, piv = lu_factor(matrix)
        return {'lu': lu.tolist(), 'piv': piv.tolist()}

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
        lu = np.array(solution['lu'])
        piv = np.array(solution['piv'])
        # Check if the provided LU factorization is correct
        reconstructed_matrix = np.array(matrix)
        n = len(matrix)
        for i in range(n):
            if piv[i] != i:
                reconstructed_matrix[[i, piv[i]]
                                     ] = reconstructed_matrix[[piv[i], i]]
        lower_triangular = np.tril(lu, -1) + np.eye(n)
        upper_triangular = np.triu(lu)
        reconstructed_lu = np.dot(lower_triangular, upper_triangular)
        return np.allclose(reconstructed_matrix, reconstructed_lu)
