
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
        # problem['A'] is the input symmetric matrix to project onto the PSD cone
        A = np.array(problem['A'])
        # Ensure symmetry
        A = (A + A.T) / 2
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(A)
        # Set negative eigenvalues to zero
        eigvals_proj = np.clip(eigvals, 0, None)
        # Reconstruct the matrix
        A_proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T
        # Ensure symmetry again due to numerical errors
        A_proj = (A_proj + A_proj.T) / 2
        return {'A_proj': A_proj}

    def is_solution(self, problem, solution):
        '''
        Check if the solution is a valid projection onto the PSD cone.
        '''
        A = np.array(problem['A'])
        A_proj = np.array(solution['A_proj'])
        # Check symmetry
        if not np.allclose(A_proj, A_proj.T, atol=1e-8):
            return False
        # Check PSD: all eigenvalues >= 0
        eigvals = np.linalg.eigvalsh(A_proj)
        if np.any(eigvals < -1e-8):
            return False
        # Check that A_proj is the closest PSD matrix to A in Frobenius norm
        # For this, check that the projection is as per the algorithm
        # (i.e., eigenvalues negative set to zero)
        A = (A + A.T) / 2
        eigvals_A, eigvecs_A = np.linalg.eigh(A)
        eigvals_proj = np.clip(eigvals_A, 0, None)
        A_proj_expected = eigvecs_A @ np.diag(eigvals_proj) @ eigvecs_A.T
        A_proj_expected = (A_proj_expected + A_proj_expected.T) / 2
        if not np.allclose(A_proj, A_proj_expected, atol=1e-8):
            return False
        return True
