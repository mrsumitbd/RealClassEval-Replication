
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def solve(self, problem):
        '''
        Given a square complex matrix, return its eigenvectors as columns of a matrix.
        Args:
            problem: a square numpy array (may have complex entries)
        Returns:
            eigenvectors: a numpy array whose columns are the eigenvectors
        '''
        # Compute eigenvectors using numpy.linalg.eig
        _, v = np.linalg.eig(problem)
        return v

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem (square numpy array)
            solution: The proposed solution (numpy array, columns are eigenvectors)
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Check shape
        if not isinstance(problem, np.ndarray) or not isinstance(solution, np.ndarray):
            return False
        if problem.shape[0] != problem.shape[1]:
            return False
        if solution.shape[0] != problem.shape[0]:
            return False
        # Check that each column is an eigenvector
        # Find eigenvalues and eigenvectors
        vals, vecs = np.linalg.eig(problem)
        # For each column in solution, check if it is an eigenvector of problem
        for i in range(solution.shape[1]):
            v = solution[:, i]
            # Ignore zero vector
            if np.allclose(v, 0):
                return False
            # Try to find a scalar lambda such that A v = lambda v
            Av = problem @ v
            # If v is an eigenvector, Av and v are collinear: Av = lambda v
            # So, lambda = Av[i]/v[i] for any i where v[i] != 0
            idx = np.where(np.abs(v) > 1e-8)[0]
            if len(idx) == 0:
                return False
            lambdas = Av[idx] / v[idx]
            # All lambdas should be (almost) equal
            if not np.allclose(lambdas, lambdas[0], atol=1e-6):
                return False
            # Check that this eigenvalue is in the spectrum
            if not np.any(np.isclose(vals, lambdas[0], atol=1e-6)):
                return False
        return True
