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
        # Return as list of eigenvectors (each as list of complex numbers)
        # Each column of eigvecs is an eigenvector
        return [eigvecs[:, i].tolist() for i in range(eigvecs.shape[1])]

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
        # Each column is an eigenvector
        eigvecs = np.array(solution, dtype=complex).T
        # For each eigenvector, check if Av = lambda v for some lambda
        for i in range(eigvecs.shape[1]):
            v = eigvecs[:, i]
            if np.allclose(v, 0):
                return False
            Av = matrix @ v
            # Find scalar lambda such that Av = lambda * v
            # If v has a nonzero entry, lambda = Av[j]/v[j]
            idx = np.flatnonzero(np.abs(v) > 1e-8)
            if len(idx) == 0:
                return False
            lambdas = Av[idx] / v[idx]
            # All lambdas should be (almost) equal
            if not np.allclose(lambdas, lambdas[0], atol=1e-6):
                return False
            # Also check Av ≈ lambda*v
            if not np.allclose(Av, lambdas[0]*v, atol=1e-6):
                return False
        return True
