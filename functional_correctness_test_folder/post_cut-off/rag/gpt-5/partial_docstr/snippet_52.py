import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, tol: float = 1e-10):
        '''Initialize the PSDConeProjection.'''
        self.tol = float(tol)

    def _get_matrix_from_problem(self, problem):
        if problem is None or not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary.")
        for key in ("matrix", "A", "M", "X"):
            if key in problem:
                mat = np.asarray(problem[key], dtype=float)
                if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
                    raise ValueError("Input matrix must be square 2D.")
                return mat
        raise KeyError(
            "Problem dictionary must contain a square matrix under one of keys: 'matrix', 'A', 'M', 'X'.")

    def _project_psd(self, A: np.ndarray, tol: float):
        A_sym = 0.5 * (A + A.T)
        # Use eigh for symmetric matrices
        w, Q = np.linalg.eigh(A_sym)
        # Clip eigenvalues
        w_clipped = np.where(w > tol, w, 0.0)
        # Reconstruct
        # Q @ diag(w_clipped) @ Q.T, using broadcasting
        X = (Q * w_clipped) @ Q.T
        # Ensure symmetry numerically
        X = 0.5 * (X + X.T)
        return X, A_sym, w, w_clipped

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        A = self._get_matrix_from_problem(problem)
        tol = float(problem.get("tol", self.tol))
        X, A_sym, w, w_clipped = self._project_psd(A, tol=tol)
        dist = float(np.linalg.norm(A_sym - X, ord="fro"))
        solution = {
            "X": X.tolist(),
            "projected_matrix": X.tolist(),
            "status": "optimal",
            "distance_fro": dist,
            "rank": int((w_clipped > tol).sum()),
            "eigenvalues_original": w.tolist(),
            "eigenvalues_projected": w_clipped.tolist(),
            "tolerance": tol,
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
            A = self._get_matrix_from_problem(problem)
        except Exception:
            return False

        # Extract projected matrix from solution
        if isinstance(solution, dict):
            X = None
            for key in ("X", "projected_matrix", "matrix", "A"):
                if key in solution:
                    X = np.asarray(solution[key], dtype=float)
                    break
            if X is None:
                return False
        else:
            X = np.asarray(solution, dtype=float)

        if X.ndim != 2 or X.shape[0] != X.shape[1]:
            return False
        if X.shape != A.shape:
            return False

        tol = float(solution.get("tolerance", self.tol)
                    ) if isinstance(solution, dict) else self.tol

        # Check symmetry
        if not np.allclose(X, X.T, atol=max(tol, 1e-12), rtol=0.0):
            return False

        # Check PSD via eigenvalues
        try:
            w, _ = np.linalg.eigh(0.5 * (X + X.T))
        except np.linalg.LinAlgError:
            return False
        if np.min(w) < -10 * max(tol, 1e-12):
            return False

        return True
