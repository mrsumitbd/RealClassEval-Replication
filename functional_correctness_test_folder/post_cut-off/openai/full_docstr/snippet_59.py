
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
                     Expected key: 'X' – a square symmetric matrix.
        Returns:
            A dictionary with key 'Y' containing the projected PSD matrix.
        '''
        if 'X' not in problem:
            raise ValueError("Problem dictionary must contain key 'X'.")

        X = np.asarray(problem['X'])
        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            raise ValueError("'X' must be a square matrix.")

        # Ensure symmetry (average with transpose)
        X_sym = 0.5 * (X + X.T)

        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(X_sym)

        # Project eigenvalues onto nonnegative orthant
        eigvals_proj = np.maximum(eigvals, 0.0)

        # Reconstruct projected matrix
        Y = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T

        # Ensure symmetry numerically
        Y = 0.5 * (Y + Y.T)

        return {'Y': Y}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution dictionary.
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Recompute the projection
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Check that solution contains 'Y'
        if 'Y' not in solution:
            return False

        Y = np.asarray(solution['Y'])
        Y_expected = np.asarray(expected['Y'])

        # Compare matrices within tolerance
        if Y.shape != Y_expected.shape:
            return False

        # Use a relative tolerance
        return np.allclose(Y, Y_expected, atol=1e-8, rtol=1e-8)
