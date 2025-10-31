
class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        self.precision = 1e-6  # Default precision for solution verification

    def solve(self, problem):
        # Placeholder for the actual solving logic
        # For demonstration, let's assume 'problem' is a matrix and we return its projection onto the PSD cone
        import numpy as np
        from scipy.linalg import sqrtm

        # Ensure the input is a numpy array
        A = np.array(problem)
        # Compute the symmetric part of the matrix
        A_sym = (A + A.T) / 2
        # Compute the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(A_sym)
        # Set negative eigenvalues to zero
        eigenvalues[eigenvalues < 0] = 0
        # Reconstruct the matrix
        projection = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
        return projection

    def is_solution(self, problem, solution):
        # Placeholder for the actual solution verification logic
        # For demonstration, let's check if the solution is symmetric and positive semi-definite
        import numpy as np

        # Check if the solution is symmetric
        if not np.allclose(solution, solution.T, atol=self.precision):
            return False
        # Check if the solution is positive semi-definite
        eigenvalues = np.linalg.eigvalsh(solution)
        if np.any(eigenvalues < -self.precision):
            return False
        return True
