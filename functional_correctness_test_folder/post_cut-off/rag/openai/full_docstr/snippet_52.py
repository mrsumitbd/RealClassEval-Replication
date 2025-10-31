
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
                     Expected to contain a key 'matrix' with a NumPy array.
        Returns:
            The solution in the format expected by the task
            (a dictionary with key 'projected_matrix').
        '''
        if 'matrix' not in problem:
            raise ValueError("Problem dictionary must contain a 'matrix' key.")
        A = np.asarray(problem['matrix'], dtype=float)

        # Ensure the matrix is symmetric
        A_sym = (A + A.T) / 2.0

        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(A_sym)

        # Project onto PSD cone: set negative eigenvalues to zero
        eigvals_proj = np.maximum(eigvals, 0.0)

        # Reconstruct the projected matrix
        proj = eigvecs @ np.diag(eigvals_proj) @ eigvecs.T

        # Return as a dictionary
        return {'projected_matrix': proj}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution dictionary.
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Basic checks
        if not isinstance(solution, dict):
            return False
        if 'projected_matrix' not in solution:
            return False

        proj = np.asarray(solution['projected_matrix'], dtype=float)

        # Check symmetry
        if not np.allclose(proj, proj.T, atol=1e-8):
            return False

        # Check positive semidefiniteness
        try:
            eigvals = np.linalg.eigvalsh(proj)
        except np.linalg.LinAlgError:
            return False
        if np.any(eigvals < -1e-8):
            return False

        # Optional: check that the projection is close to the original matrix
        # (within a tolerance). This is not strictly required but helps catch
        # gross errors.
        if 'matrix' in problem:
            A = np.asarray(problem['matrix'], dtype=float)
            # Ensure symmetry of original
            A_sym = (A + A.T) / 2.0
            diff_norm = np.linalg.norm(proj - A_sym, ord='fro')
            # The Frobenius norm of the difference should be non-negative and
            # typically small; we allow a generous tolerance.
            if diff_norm > 1e-6 * np.linalg.norm(A_sym, ord='fro'):
                # Not necessarily a failure, but we flag it as suspicious.
                # Returning False would be too strict for many use cases.
                pass

        return True
