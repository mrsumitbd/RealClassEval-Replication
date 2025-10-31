
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
        self.matrix = problem.get('matrix')
        if self.matrix is None:
            raise ValueError("Matrix not provided in the problem data")

        # Convert the matrix to a numpy array if it's not already
        if not isinstance(self.matrix, np.ndarray):
            self.matrix = np.array(self.matrix, dtype=complex)

        # Compute eigenvalues and eigenvectors
        self.eigenvalues, self.eigenvectors = np.linalg.eig(self.matrix)

        # Return the solution in the expected format
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
        if not isinstance(solution, dict):
            return False

        eigenvalues = solution.get('eigenvalues')
        eigenvectors = solution.get('eigenvectors')

        if eigenvalues is None or eigenvectors is None:
            return False

        # Check if the number of eigenvalues matches the matrix size
        if len(eigenvalues) != len(problem['matrix']):
            return False

        # Check if the number of eigenvectors matches the matrix size
        if len(eigenvectors) != len(problem['matrix']):
            return False

        # Check if each eigenvector has the correct length
        for vec in eigenvectors:
            if len(vec) != len(problem['matrix']):
                return False

        # Verify that each eigenvalue and eigenvector pair satisfies A*v = λ*v
        for i in range(len(eigenvalues)):
            lambda_i = eigenvalues[i]
            v_i = np.array(eigenvectors[i], dtype=complex)
            Av = np.dot(problem['matrix'], v_i)
            lambda_v = lambda_i * v_i
            if not np.allclose(Av, lambda_v, atol=1e-6):
                return False

        return True
