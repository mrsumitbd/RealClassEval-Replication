
import numpy as np


class EigenvectorsComplex:

    def __init__(self):
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
        return {'eigenvalues': eigenvalues.tolist(), 'eigenvectors': eigenvectors.tolist()}

    def is_solution(self, problem, solution):
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues = np.array(solution['eigenvalues'], dtype=complex)
        eigenvectors = np.array(solution['eigenvectors'], dtype=complex)

        # Check if the eigenvalues and eigenvectors satisfy the equation Ax = λx
        for i in range(len(eigenvalues)):
            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[:, i]
            product = np.dot(matrix, eigenvector)
            expected_product = eigenvalue * eigenvector

            # Check if the two products are close enough
            if not np.allclose(product, expected_product):
                return False

        return True
