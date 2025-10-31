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
        # Expecting problem to have a key 'matrix' with a 2D list or np.ndarray
        matrix = np.array(problem['matrix'], dtype=complex)
        eigvals, eigvecs = np.linalg.eig(matrix)
        # Return as list of lists (columns are eigenvectors)
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
        # Each column of eigvecs should be an eigenvector: A v = lambda v for some lambda
        # We'll check for each column if Av is proportional to v
        for i in range(eigvecs.shape[1]):
            v = eigvecs[:, i]
            Av = matrix @ v
            # Try to find lambda: if v is not all zeros
            if np.allclose(v, 0):
                continue
            # lambda = (Av / v) where v != 0
            nonzero = np.abs(v) > 1e-8
            if not np.any(nonzero):
                continue
            ratios = Av[nonzero] / v[nonzero]
            # All ratios should be (almost) equal
            if not np.allclose(ratios, ratios[0], atol=1e-6):
                return False
        return True
