import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        self.atol = 1e-8
        self.rtol = 1e-7

    def _extract_matrix(self, problem):
        for key in ('matrix', 'A', 'M', 'X', 'Q'):
            if key in problem:
                return np.asarray(problem[key])
        if isinstance(problem, np.ndarray):
            return problem
        if isinstance(problem, (list, tuple)):
            arr = np.asarray(problem)
            if arr.ndim == 2:
                return arr
        raise ValueError(
            "Problem must contain a matrix under one of keys: 'matrix', 'A', 'M', 'X', 'Q'")

    def _symmetrize(self, A):
        if np.iscomplexobj(A):
            return 0.5 * (A + A.conj().T)
        return 0.5 * (A + A.T)

    def _project_psd(self, A):
        A = self._symmetrize(A)
        n, m = A.shape
        if n != m:
            raise ValueError("Input matrix must be square.")
        try:
            w, V = np.linalg.eigh(A)
        except np.linalg.LinAlgError:
            jitter = 1e-8 * np.eye(n, dtype=A.dtype)
            w, V = np.linalg.eigh(A + jitter)
        w_clipped = np.clip(w, 0, None)
        X = (V * w_clipped) @ V.conj().T
        X = self._symmetrize(X)
        return X, w, w_clipped

    def _fro_norm(self, M):
        return np.linalg.norm(M, ord='fro')

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        A = self._extract_matrix(problem)
        X, w, w_clipped = self._project_psd(A)
        A_sym = self._symmetrize(np.asarray(A))
        distance = self._fro_norm(X - A_sym)
        return {
            'projected_matrix': X,
            'distance': float(distance),
            'status': 'optimal',
            'eigenvalues': w,
            'clipped_eigenvalues': w_clipped
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = self._extract_matrix(problem)

        if isinstance(solution, dict):
            X = solution.get('projected_matrix', None)
            if X is None:
                # try common alternatives
                X = solution.get('X', solution.get('matrix', None))
        else:
            X = solution

        if X is None:
            return False

        X = np.asarray(X)
        A = np.asarray(A)

        if X.shape != A.shape or X.ndim != 2 or X.shape[0] != X.shape[1]:
            return False

        # Symmetry check
        if np.iscomplexobj(X):
            if not np.allclose(X, X.conj().T, atol=self.atol, rtol=self.rtol):
                return False
        else:
            if not np.allclose(X, X.T, atol=self.atol, rtol=self.rtol):
                return False

        # PSD check
        try:
            wX = np.linalg.eigvalsh(self._symmetrize(X))
        except np.linalg.LinAlgError:
            return False
        if np.min(wX).real < -10 * self.atol:
            return False

        # Optimality check: should equal our projection within tolerance
        X_star, _, _ = self._project_psd(A)
        denom = 1.0 + self._fro_norm(X_star)
        if self._fro_norm(X - X_star) > 1e-6 * denom:
            return False

        return True
