
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
        Checks if the solution is a PSD matrix and is the closest PSD matrix to the input.
        For practical purposes, checks if the matrix is symmetric and all eigenvalues >= -1e-8.
        """
        X = problem['matrix']
        X_proj = solution['matrix']
        # Check symmetry
        if not np.allclose(X_proj, X_proj.T, atol=1e-8):
            return False
        # Check PSD
        eigvals = np.linalg.eigvalsh(X_proj)
        if np.min(eigvals) < -1e-8:
            return False
        # Check optimality: X_proj should be the closest PSD matrix to X in Frobenius norm
        # Project X onto PSD cone again and check closeness
        test_proj = self.solve({'matrix': X})['matrix']
        if not np.allclose(test_proj, X_proj, atol=1e-8):
            return False
        return True
