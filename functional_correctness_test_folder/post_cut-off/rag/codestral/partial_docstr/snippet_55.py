
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        self.matrix = None
        self.eigenvalues = None
        self.eigenvectors = None

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        self.matrix = np.array(problem['matrix'], dtype=complex)
        self.eigenvalues, self.eigenvectors = np.linalg.eig(self.matrix)
        return {
            'eigenvalues': self.eigenvalues.tolist(),
            'eigenvectors': self.eigenvectors.tolist()
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
        if not all(key in solution for key in ['eigenvalues', 'eigenvectors']):
            return False

        original_matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues = np.array(solution['eigenvalues'], dtype=complex)
        eigenvectors = np.array(solution['eigenvectors'], dtype=complex)

        if eigenvalues.shape[0] != original_matrix.shape[0]:
            return False

        if eigenvectors.shape != original_matrix.shape:
            return False

        for i in range(len(eigenvalues)):
            reconstructed = eigenvalues[i] * eigenvectors[:, i]
            original_column = original_matrix[:, i]
            if not np.allclose(reconstructed, original_column):
                return False

        return True
