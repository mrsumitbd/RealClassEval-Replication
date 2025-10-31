import numpy as np


class PSDConeProjection:

    def __init__(self, tol=1e-8, rel_tol=1e-7):
        self.tol = tol
        self.rel_tol = rel_tol

    def _get_matrix_from_problem(self, problem):
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")
        for k in ('X', 'M', 'A', 'matrix', 'input', 'S'):
            if k in problem:
                M = np.array(problem[k], dtype=float)
                break
        else:
            raise KeyError(
                "Problem dict must contain a matrix under one of keys: 'X','M','A','matrix','input','S'")
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            raise ValueError("Input matrix must be square 2D array")
        symmetric = problem.get('symmetric', False)
        if symmetric:
            return M
        return 0.5 * (M + M.T)

    def _project_psd(self, M):
        # Eigendecomposition of symmetric matrix
        w, V = np.linalg.eigh(M)
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
        M = self._get_matrix_from_problem(problem)
        X, evals, evals_proj = self._project_psd(M)
        return {'X': X, 'eigvals': evals, 'eigvals_proj': evals_proj}

    def is_solution(self, problem, solution):
        if not isinstance(solution, dict):
            return False
        # Extract candidate solution matrix
        cand = None
        for k in ('X', 'matrix', 'M', 'A'):
            if k in solution:
                cand = np.array(solution[k], dtype=float)
                break
        if cand is None:
            return False
        if cand.ndim != 2 or cand.shape[0] != cand.shape[1]:
            return False

        # Symmetry check
        sym_err = np.linalg.norm(cand - cand.T, ord='fro')
        nrm = max(1.0, np.linalg.norm(cand, ord='fro'))
        if sym_err > self.rel_tol * nrm + self.tol:
            return False

        # PSD check
        cand_sym = 0.5 * (cand + cand.T)
        try:
            w = np.linalg.eigh(cand_sym, UPLO='U')[0]
        except Exception:
            w = np.linalg.eigvalsh(cand_sym)
        if np.min(w) < -10 * (self.rel_tol * nrm + self.tol):
            return False

        # Optimality check by re-projecting and comparing
        M = self._get_matrix_from_problem(problem)
        X_star, _, _ = self._project_psd(M)
        diff = np.linalg.norm(cand_sym - X_star, ord='fro')
        base = max(1.0, np.linalg.norm(M, ord='fro'))
        return diff <= 10 * (self.rel_tol * base + self.tol)
