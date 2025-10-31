
class PSDConeProjection:

    def __init__(self):
        self.tolerance = 1e-6

    def solve(self, problem):
        import numpy as np
        # Assuming problem is a symmetric matrix that needs to be projected onto the PSD cone
        eigenvalues, eigenvectors = np.linalg.eigh(problem)
        # Project eigenvalues to be non-negative
        eigenvalues = np.maximum(eigenvalues, 0)
        solution = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
        return solution

    def is_solution(self, problem, solution):
        import numpy as np
        # Check if solution is symmetric
        if not np.allclose(solution, solution.T, atol=self.tolerance):
            return False
        # Check if solution is positive semi-definite
        eigenvalues = np.linalg.eigvalsh(solution)
        if np.any(eigenvalues < -self.tolerance):
            return False
        # Check if the solution is the closest point in the PSD cone to the problem
        diff = solution - problem
        if not np.allclose(diff @ problem, 0, atol=self.tolerance):
            return False
        return True
