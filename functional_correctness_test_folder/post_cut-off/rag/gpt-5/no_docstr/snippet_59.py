import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        self.tol = 1e-10

    def _extract_matrix(self, problem):
        keys = ['A', 'matrix', 'M', 'input', 'data']
        for k in keys:
            if k in problem:
                return problem[k], k
        raise KeyError(
            "Problem dictionary must contain one of keys: 'A', 'matrix', 'M', 'input', or 'data'.")

    def _to_numpy(self, mat):
        if isinstance(mat, np.ndarray):
            return mat, 'numpy'
        arr = np.array(mat, dtype=float)
        return arr, 'list'

    def _return_as(self, arr, original_kind):
        if original_kind == 'numpy':
            return arr
        return arr.tolist()

    def _project_psd(self, A):
        A = (A + A.T) / 2.0
        # eigh for symmetric matrices
        w, V = np.linalg.eigh(A)
        w_clipped = np.clip(w, 0.0, None)
        X = (V * w_clipped) @ V.T
        # Ensure symmetry numerically
        X = (X + X.T) / 2.0
        return X

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        A_raw, key = self._extract_matrix(problem)
        A, kind = self._to_numpy(A_raw)

        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix must be square.")

        X = self._project_psd(A)
        return {'X': self._return_as(X, kind)}

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
            A_raw, _ = self._extract_matrix(problem)
            A, _ = self._to_numpy(A_raw)

            if not isinstance(solution, dict):
                return False
            if 'X' not in solution:
                # accept some flexibility on key naming
                candidate_keys = ['matrix', 'projected', 'psd', 'solution']
                found = None
                for k in candidate_keys:
                    if k in solution:
                        found = k
                        break
                if found is None:
                    return False
                X_raw = solution[found]
            else:
                X_raw = solution['X']

            X, _ = self._to_numpy(X_raw)

            if A.ndim != 2 or A.shape[0] != A.shape[1]:
                return False
            if X.shape != A.shape:
                return False

            # Symmetrize both
            A_sym = (A + A.T) / 2.0
            X_sym = (X + X.T) / 2.0

            # Check symmetry
            if np.linalg.norm(X - X_sym, ord='fro') > 1e-8 * max(1.0, np.linalg.norm(X, ord='fro')):
                return False

            # Check X is PSD
            wX = np.linalg.eigvalsh(X_sym)
            if np.min(wX) < -1e-8 * max(1.0, np.max(np.abs(wX))):
                return False

            # KKT optimality for Euclidean projection:
            # R = A_sym - X_sym must be negative semidefinite
            R = A_sym - X_sym
            wR = np.linalg.eigvalsh((R + R.T) / 2.0)
            if np.max(wR) > 1e-8 * max(1.0, np.max(np.abs(wR))):
                return False

            # Orthogonality: trace(X R) approx 0
            tr = float(np.trace(X_sym @ R))
            if abs(tr) > 1e-6 * (np.linalg.norm(X_sym, ord='fro') * np.linalg.norm(R, ord='fro') + 1e-12):
                return False

            return True
        except Exception:
            return False
