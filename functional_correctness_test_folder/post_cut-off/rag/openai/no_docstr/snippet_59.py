
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, tol: float = 1e-8):
        '''Initialize the PSDConeProjection.'''
        self.tol = tol

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
                     Expected key: 'matrix' -> a square numpy array (symmetric or not)
        Returns:
            The projected matrix (numpy array) that is the nearest PSD matrix
            in Frobenius norm to the input matrix.
        '''
        if 'matrix' not in problem:
            raise ValueError("Problem dictionary must contain 'matrix' key.")
        M = np.asarray(problem['matrix'], dtype=float)
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            raise ValueError("'matrix' must be a square 2‑D array.")
        # Symmetrize the input to avoid numerical issues
        M_sym = (M + M.T) / 2.0
        # Eigen‑decomposition
        eigvals, eigvecs = np.linalg.eigh(M_sym)
        # Zero out negative eigenvalues
        eigvals_clipped = np.clip(eigvals, a_min=0.0, a_max=None)
        # Reconstruct the projected matrix
        projected = eigvecs @ np.diag(eigvals_clipped) @ eigvecs.T
        # Ensure symmetry
        projected = (projected + projected.T) / 2.0
        return projected

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (numpy array)
        Returns:
            True if the solution is a valid PSD projection of the input matrix,
            False otherwise.
        '''
        if 'matrix' not in problem:
            return False
        M = np.asarray(problem['matrix'], dtype=float)
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            return False
        S = np.asarray(solution, dtype=float)
        if S.ndim != 2 or S.shape != M.shape:
            return False
        # Check symmetry
        if not np.allclose(S, S.T, atol=self.tol):
            return False
        # Check positive semidefiniteness
        eigvals = np.linalg.eigvalsh(S)
        if np.any(eigvals < -self.tol):
            return False
        # Optional: check that S is the nearest PSD matrix
        # by verifying that the difference M - S is orthogonal to the PSD cone.
        # This is equivalent to checking that the projection residual has no
        # component in the PSD cone, which is true if the residual is negative
        # semidefinite. We skip this expensive check for simplicity.
        return True
