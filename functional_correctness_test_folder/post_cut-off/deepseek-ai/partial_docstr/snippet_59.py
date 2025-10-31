
import numpy as np


class PSDConeProjection:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        X = problem['X']
        n = X.shape[0]
        eigvals, eigvecs = np.linalg.eigh(X)
        eigvals_proj = np.maximum(eigvals, 0)
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        return X_proj

    def is_solution(self, problem, solution):
        X_proj = solution
        if not np.allclose(X_proj, X_proj.T):
            return False
        eigvals = np.linalg.eigvalsh(X_proj)
        if np.any(eigvals < -1e-10):
            return False
        return True
