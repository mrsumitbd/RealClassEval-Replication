
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Given a symmetric matrix in 'problem', project it onto the PSD cone.
        problem: dict with key 'matrix' containing a square numpy array.
        Returns: dict with key 'matrix' containing the projected matrix.
        """
        A = problem['matrix']
        # Ensure symmetry
        A = (A + A.T) / 2
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(A)
        # Set negative eigenvalues to zero
        eigvals_proj = np.clip(eigvals, 0, None)
        # Reconstruct the matrix
        A_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry
        A_proj = (A_proj + A_proj.T) / 2
        return {'matrix': A_proj}

    def is_solution(self, problem, solution):
        """
        Checks if the solution is a valid PSD projection of the problem matrix.
        Returns True if:
        - The solution matrix is symmetric
        - The solution matrix is positive semidefinite (all eigenvalues >= 0)
        """
        A_proj = solution['matrix']
        # Check symmetry
        if not np.allclose(A_proj, A_proj.T, atol=1e-8):
            return False
        # Check positive semidefiniteness
        eigvals = np.linalg.eigvalsh(A_proj)
        if np.all(eigvals >= -1e-8):
            return True
        return False
