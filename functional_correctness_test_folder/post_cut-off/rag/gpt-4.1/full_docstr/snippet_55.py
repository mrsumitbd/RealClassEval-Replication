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
        # Expecting problem['matrix'] to be a 2D list or np.ndarray of complex numbers
        matrix = np.array(problem['matrix'], dtype=complex)
        # Compute eigenvalues and right eigenvectors
        eigvals, eigvecs = np.linalg.eig(matrix)
        # Return as lists for serialization
        return {
            'eigenvalues': eigvals.tolist(),
            'eigenvectors': eigvecs.tolist()
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
        matrix = np.array(problem['matrix'], dtype=complex)
        eigvals = np.array(solution['eigenvalues'], dtype=complex)
        eigvecs = np.array(solution['eigenvectors'], dtype=complex)
        # Check shape
        if eigvecs.shape[0] != matrix.shape[0]:
            return False
        if eigvecs.shape[1] != len(eigvals):
            return False
        # Check that A v = lambda v for each eigenpair (up to numerical tolerance)
        for i in range(len(eigvals)):
            v = eigvecs[:, i]
            lam = eigvals[i]
            Av = matrix @ v
            lv = lam * v
            if not np.allclose(Av, lv, atol=1e-6):
                return False
        return True
