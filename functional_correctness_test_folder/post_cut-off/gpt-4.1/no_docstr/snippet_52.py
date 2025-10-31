
import numpy as np


class PSDConeProjection:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Given a symmetric matrix in 'problem', project it onto the PSD cone.
        'problem' is expected to be a dict with key 'matrix' mapping to a numpy array.
        Returns a dict with key 'matrix' mapping to the projected matrix.
        """
        X = problem['matrix']
        # Ensure symmetry
        X_sym = (X + X.T) / 2
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X_sym)
        # Project eigenvalues onto nonnegative orthant
        eigvals_proj = np.clip(eigvals, 0, None)
        # Reconstruct the matrix
        X_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry
        X_proj = (X_proj + X_proj.T) / 2
        return {'matrix': X_proj}

    def is_solution(self, problem, solution):
        """
        Checks if the matrix in 'solution' is a valid projection of the matrix in 'problem' onto the PSD cone.
        Returns True if the solution is symmetric and PSD, False otherwise.
        """
        X_proj = solution['matrix']
        # Check symmetry
        if not np.allclose(X_proj, X_proj.T, atol=1e-8):
            return False
        # Check positive semidefiniteness (all eigenvalues >= 0)
        eigvals = np.linalg.eigvalsh(X_proj)
        if np.all(eigvals >= -1e-8):
            return True
        return False
