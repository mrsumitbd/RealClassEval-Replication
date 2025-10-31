
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
                - 'matrix': the symmetric matrix to project onto the PSD cone
        Returns:
            The solution in the format expected by the task
                - 'projected_matrix': the nearest PSD matrix
        '''
        A = np.array(problem['matrix'])
        # Ensure symmetry
        A = (A + A.T) / 2
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(A)
        # Set negative eigenvalues to zero
        eigvals_clipped = np.clip(eigvals, 0, None)
        # Reconstruct the matrix
        projected = eigvecs @ np.diag(eigvals_clipped) @ eigvecs.T
        # Ensure symmetry again due to numerical errors
        projected = (projected + projected.T) / 2
        return {'projected_matrix': projected}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        projected = np.array(solution['projected_matrix'])
        # Check symmetry
        if not np.allclose(projected, projected.T, atol=1e-8):
            return False
        # Check positive semidefiniteness (all eigenvalues >= 0)
        eigvals = np.linalg.eigvalsh(projected)
        if np.all(eigvals >= -1e-8):
            return True
        return False
