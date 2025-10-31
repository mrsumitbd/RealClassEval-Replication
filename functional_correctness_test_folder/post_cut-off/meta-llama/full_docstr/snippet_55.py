
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
        # Sort eigenvalues and eigenvectors based on the eigenvalues
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
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

        # Check if the number of eigenvalues and eigenvectors match the matrix size
        if len(eigenvalues) != matrix.shape[0] or eigenvectors.shape[0] != matrix.shape[0] or eigenvectors.shape[1] != matrix.shape[0]:
            return False

        # Check if the eigenvectors are correct
        for i in range(len(eigenvalues)):
            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[:, i]
            # Check if the eigenvector is not zero
            if np.allclose(eigenvector, 0):
                return False
            # Check if the eigenvector satisfies the equation Ax = λx
            if not np.allclose(np.dot(matrix, eigenvector), eigenvalue * eigenvector):
                return False

        return True
