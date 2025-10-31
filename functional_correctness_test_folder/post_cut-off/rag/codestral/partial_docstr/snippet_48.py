
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
        matrix = problem.get('matrix')
        if matrix is None:
            raise ValueError("Problem must contain a 'matrix' key")

        # Convert the input to a numpy array if it isn't already
        matrix = np.array(matrix, dtype=complex)

        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(matrix)

        # Normalize the eigenvectors
        for i in range(eigenvectors.shape[1]):
            eigenvectors[:, i] = eigenvectors[:, i] / \
                np.linalg.norm(eigenvectors[:, i])

        # Prepare the solution
        solution = {
            'eigenvalues': eigenvalues.tolist(),
            'eigenvectors': eigenvectors.T.tolist()  # Transpose to match expected format
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
        if not isinstance(solution, dict):
            return False

        required_keys = {'eigenvalues', 'eigenvectors'}
        if not all(key in solution for key in required_keys):
            return False

        matrix = np.array(problem.get('matrix', []), dtype=complex)
        eigenvalues = np.array(solution['eigenvalues'], dtype=complex)
        eigenvectors = np.array(solution['eigenvectors'], dtype=complex).T

        # Check if the number of eigenvalues matches the matrix size
        if len(eigenvalues) != matrix.shape[0]:
            return False

        # Check if the number of eigenvectors matches the matrix size
        if eigenvectors.shape[1] != matrix.shape[0]:
            return False

        # Check if each eigenvector is indeed an eigenvector
        for i in range(len(eigenvalues)):
            ev = eigenvectors[:, i]
            if not np.allclose(matrix @ ev, eigenvalues[i] * ev):
                return False

        return True
