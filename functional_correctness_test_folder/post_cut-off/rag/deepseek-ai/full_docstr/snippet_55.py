
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
        matrix = np.array(problem['matrix'], dtype=np.complex128)
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
        matrix = np.array(problem['matrix'], dtype=np.complex128)
        eigenvalues = np.array(solution['eigenvalues'], dtype=np.complex128)
        eigenvectors = np.array(solution['eigenvectors'], dtype=np.complex128)

        for i in range(len(eigenvalues)):
            eigenvector = eigenvectors[:, i]
            lhs = np.dot(matrix, eigenvector)
            rhs = eigenvalues[i] * eigenvector
            if not np.allclose(lhs, rhs, atol=1e-6):
                return False
        return True
