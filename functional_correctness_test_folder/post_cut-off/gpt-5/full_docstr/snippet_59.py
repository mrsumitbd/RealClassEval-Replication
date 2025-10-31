import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        self.default_tol = 1e-8

    def _to_numpy_matrix(self, A):
        A_np = np.array(A, dtype=float)
        if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
            raise ValueError("Input matrix must be a square 2D array.")
        return A_np

    def _project_to_psd(self, A):
        A_sym = 0.5 * (A + A.T)
        w, V = np.linalg.eigh(A_sym)
        w_clipped = np.maximum(w, 0.0)
        X = (V * w_clipped) @ V.T
        X = 0.5 * (X + X.T)
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
            raise TypeError("problem must be a dict.")
        if "A" not in problem:
            raise KeyError("problem must contain key 'A'.")

        A = self._to_numpy_matrix(problem["A"])
        X, w, w_clipped = self._project_to_psd(A)

        solution = {"X": X}
        if problem.get("return_eigvals", False):
            solution["eigvals_original"] = w
            solution["eigvals_projected"] = w_clipped
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
        try:
            A = self._to_numpy_matrix(problem["A"])
        except Exception:
            return False

        # Accept solution as dict with 'X' or a raw matrix-like.
        if isinstance(solution, dict):
            if "X" not in solution:
                return False
            X = np.array(solution["X"], dtype=float)
        else:
            X = np.array(solution, dtype=float)

        if X.ndim != 2 or X.shape != A.shape:
            return False

        tol = float(problem.get("tolerance", self.default_tol))

        # Check symmetry
        if not np.allclose(X, X.T, atol=tol, rtol=0):
            return False

        # Check PSD via eigenvalues
        try:
            wX = np.linalg.eigh(0.5 * (X + X.T))[0]
        except np.linalg.LinAlgError:
            return False
        if np.min(wX) < -10 * tol:
            return False

        # Check it matches the standard PSD projection of A
        X_proj, _, _ = self._project_to_psd(A)
        if not np.allclose(X, X_proj, atol=10 * tol, rtol=0):
            # Allow relative tolerance based on A's norm if nonzero
            normA = np.linalg.norm(A, 'fro')
            rtol = 10 * tol if normA > 0 else 0
            if not np.allclose(X, X_proj, atol=10 * tol, rtol=rtol):
                return False

        return True
