class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, rtol=1e-8, atol=1e-10):
        import numpy as np  # for IDEs that analyze imports
        self.rtol = float(rtol)
        self.atol = float(atol)

    def _to_array(self, M):
        import numpy as np
        arr = np.array(M, dtype=float)
        if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
            raise ValueError("Input must be a square 2D matrix.")
        return arr

    def _symmetrize(self, A):
        return 0.5 * (A + A.T)

    def _project_psd(self, A):
        import numpy as np
        A = self._to_array(A)
        A = self._symmetrize(A)
        # Use eigh for symmetric matrices
        vals, vecs = np.linalg.eigh(A)
        vals_clipped = np.clip(vals, 0.0, None)
        # Reconstruct positive part
        Ap = (vecs * vals_clipped) @ vecs.T
        # Ensure symmetry numerically
        Ap = self._symmetrize(Ap)
        return Ap

    def solve(self, problem):
        M = problem.get("matrix", None) if isinstance(
            problem, dict) else problem
        if M is None:
            raise ValueError(
                "Problem must contain key 'matrix' or be a matrix itself.")
        return self._project_psd(M)

    def _is_psd(self, A):
        import numpy as np
        A = self._to_array(A)
        A = self._symmetrize(A)
        # Small negative eigenvalues allowed within tolerance
        try:
            vals = np.linalg.eigvalsh(A)
        except np.linalg.LinAlgError:
            return False
        return np.all(vals >= -max(self.rtol * np.max(np.abs(vals)), self.atol))

    def is_solution(self, problem, solution):
        import numpy as np
        # Validate solution type and shape
        try:
            S = self._to_array(solution)
        except Exception:
            return False

        # PSD check
        if not self._is_psd(S):
            return False

        # Recompute projection and compare
        try:
            P = self.solve(problem)
        except Exception:
            return False

        if P.shape != S.shape:
            return False

        diff = np.linalg.norm(P - S, ord='fro')
        base = max(np.linalg.norm(P, ord='fro'), 1.0)
        return diff <= self.rtol * base + self.atol
