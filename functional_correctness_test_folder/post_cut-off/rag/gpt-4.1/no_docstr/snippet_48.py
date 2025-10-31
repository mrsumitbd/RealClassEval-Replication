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
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        # Expecting problem['matrix'] to be a list of lists or np.ndarray
        matrix = np.array(problem['matrix'], dtype=complex)
        eigvals, eigvecs = np.linalg.eig(matrix)
        # Return as list of lists (each column is an eigenvector)
        return eigvecs.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        matrix = np.array(problem['matrix'], dtype=complex)
        eigvecs = np.array(solution, dtype=complex)
        # Each column of eigvecs is an eigenvector
        # Check if A v = lambda v for some lambda
        for i in range(eigvecs.shape[1]):
            v = eigvecs[:, i]
            if np.allclose(v, 0):
                continue
            Av = matrix @ v
            # Try to find lambda: Av = lambda v
            # If v is not zero, lambda = (Av / v) (elementwise), but need to check all elements are (almost) equal
            nonzero = np.abs(v) > 1e-8
            if not np.any(nonzero):
                continue
            ratios = Av[nonzero] / v[nonzero]
            if not np.allclose(ratios, ratios[0]):
                return False
        return True
