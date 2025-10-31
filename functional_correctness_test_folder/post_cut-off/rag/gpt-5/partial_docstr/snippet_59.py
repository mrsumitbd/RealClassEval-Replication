import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, tol: float = 1e-8):
        '''Initialize the PSDConeProjection.'''
        self.tol = float(tol)

    def _get_matrix_from_problem(self, problem):
        if not isinstance(problem, dict):
            raise TypeError("Problem must be a dictionary.")
        # Try common keys
        for key in ("matrix", "M", "A", "X", "input"):
            if key in problem:
                M = np.array(problem[key])
                break
        else:
            raise KeyError(
                "Problem dictionary must contain one of the keys: 'matrix', 'M', 'A', 'X', 'input'.")
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            raise ValueError(
                "Input matrix must be square (2D with equal dimensions).")
        return M

    def _symmetrize(self, M):
        if np.iscomplexobj(M):
            return 0.5 * (M + M.conj().T)
        return 0.5 * (M + M.T)

    def _project_psd(self, M):
        S = self._symmetrize(M)
        # eigh for Hermitian; handles real symmetric and complex Hermitian
        w, V = np.linalg.eigh(S)
        w_clipped = np.maximum(w, 0.0)
        # Reconstruct: V diag(w_clipped) V^H
        X = (V * w_clipped) @ V.conj().T
        # Ensure symmetry numerically
        X = self._symmetrize(X)
        return X, w, w_clipped, V

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        M = self._get_matrix_from_problem(problem)
        X, w, w_clipped, V = self._project_psd(M)
        residual = self._symmetrize(M) - X
        frob_dist = float(np.linalg.norm(residual, ord="fro"))
        solution = {
            "projected_matrix": X,
            "X": X,
            "matrix": X,
            "eigenvalues": w,
            "eigenvalues_clipped": w_clipped,
            "eigenvectors": V,
            "distance_fro": frob_dist,
            "status": "optimal",
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
        try:
            M = self._get_matrix_from_problem(problem)
        except Exception:
            return False

        if not isinstance(solution, dict):
            return False

        # Try to extract candidate solution matrix
        X = None
        for key in ("projected_matrix", "X", "matrix"):
            if key in solution:
                X = np.array(solution[key])
                break
        if X is None:
            return False

        if X.ndim != 2 or X.shape != M.shape:
            return False

        # Symmetry check
        X_sym = self._symmetrize(X)
        sym_err = np.linalg.norm(X - X_sym, ord="fro")
        scale = max(1.0, np.linalg.norm(X_sym, ord="fro"))
        if sym_err > self.tol * scale:
            return False

        # PSD check: eigenvalues >= -tol
        try:
            w, _ = np.linalg.eigh(X_sym)
        except np.linalg.LinAlgError:
            return False
        if np.min(w) < -10 * self.tol:
            return False

        # Optimality check by reprojection
        Y, _, _, _ = self._project_psd(M)
        diff = np.linalg.norm(X_sym - Y, ord="fro")
        scale_y = max(1.0, np.linalg.norm(Y, ord="fro"))
        if diff > 5 * self.tol * scale_y:
            return False

        return True
