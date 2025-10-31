import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, atol: float = 1e-10, rtol: float = 1e-8):
        '''Initialize the PSDConeProjection.'''
        self.atol = atol
        self.rtol = rtol

    def _symmetrize(self, A: np.ndarray) -> np.ndarray:
        if np.iscomplexobj(A):
            return 0.5 * (A + A.conj().T)
        return 0.5 * (A + A.T)

    def _project_psd(self, A: np.ndarray):
        A = self._symmetrize(A)
        # Use eigh for Hermitian; it guarantees real eigenvalues for Hermitian input
        w, V = np.linalg.eigh(A)
        # Clip small negative eigenvalues due to numerical errors
        tol = self.atol + self.rtol * \
            max(1.0, np.abs(w).max() if w.size else 0.0)
        w_clipped = np.where(w > tol, w, 0.0)
        X = (V * w_clipped) @ V.conj().T
        # Ensure symmetry numerically
        X = self._symmetrize(np.real_if_close(X))
        return X, w, w_clipped

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary.")

        # Accept common keys
        A = problem.get('matrix', None)
        if A is None:
            A = problem.get('A', None)
        if A is None:
            A = problem.get('X', None)
        if A is None:
            raise ValueError(
                "Problem must contain a key 'matrix', 'A', or 'X' with the input matrix.")

        A = np.asarray(A)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix must be a square 2D array.")

        X, w, w_clipped = self._project_psd(A)

        solution = {
            'X': X,
            'eigenvalues': w,
            'eigenvalues_clipped': w_clipped,
            'rank': int(np.count_nonzero(w_clipped > 0.0)),
            'status': 'solved'
        }
        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(problem, dict) or not isinstance(solution, dict):
            return False

        X = solution.get('X', None)
        if X is None:
            return False

        X = np.asarray(X)
        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            return False

        # Check symmetry
        if not np.allclose(X, self._symmetrize(X), atol=self.atol, rtol=self.rtol):
            return False

        # Check PSD (all eigenvalues >= -tol)
        wX = np.linalg.eigvalsh(self._symmetrize(X))
        tol_psd = self.atol + self.rtol * \
            max(1.0, np.abs(wX).max() if wX.size else 0.0)
        if np.any(wX < -tol_psd):
            return False

        # If original problem contains matrix, verify it matches projection
        A = problem.get('matrix', None)
        if A is None:
            A = problem.get('A', None)
        if A is None:
            A = problem.get('X', None)

        if A is None:
            # Without original data, we can only assert PSD and symmetry
            return True

        A = np.asarray(A)
        if A.shape != X.shape:
            return False

        X_star, _, _ = self._project_psd(A)
        return np.allclose(X, X_star, atol=self.atol, rtol=self.rtol)
