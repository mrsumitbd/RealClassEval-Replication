
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
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        solution = {
            'eigenvalues': eigenvalues.tolist(),
            'eigenvectors': eigenvectors.tolist()
        }
        return solution

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
        eigenvalues = np.array(solution['eigenvalues'], dtype=complex)
        eigenvectors = np.array(solution['eigenvectors'], dtype=complex)

        for i in range(len(eigenvalues)):
            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[:, i]
            if not np.allclose(matrix @ eigenvector, eigenvalue * eigenvector, atol=1e-6):
                return False
        return True
