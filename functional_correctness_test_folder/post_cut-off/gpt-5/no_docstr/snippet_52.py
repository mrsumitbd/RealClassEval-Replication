import numpy as np


class PSDConeProjection:

    def __init__(self, tol: float = 1e-9):
        self.tol = float(tol)

    def solve(self, problem):
        A = np.asarray(problem)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input must be a square 2D array.")
        if not np.all(np.isfinite(A)):
            raise ValueError("Input contains non-finite values.")
        # Symmetrize
        S = 0.5 * (A + A.T)
        # Eigen-decomposition
        try:
            w, Q = np.linalg.eigh(S)
        except np.linalg.LinAlgError as e:
            raise ValueError(f"Eigendecomposition failed: {e}")
        # Clip eigenvalues
        w_clipped = np.where(w > self.tol, w, 0.0)
        X = (Q * w_clipped) @ Q.T
        # Ensure symmetry numerically
        X = 0.5 * (X + X.T)
        return X

    def is_solution(self, problem, solution):
        A = np.asarray(problem)
        X = np.asarray(solution)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        if X.shape != A.shape:
            return False
        if not (np.all(np.isfinite(A)) and np.all(np.isfinite(X))):
            return False
        # Check symmetry of solution
        normX = np.linalg.norm(X, ord='fro')
        if np.linalg.norm(X - X.T, ord='fro') > self.tol * max(1.0, normX):
            return False
        # Check PSD: smallest eigenvalue >= -tol * scale
        try:
            w = np.linalg.eigvalsh(0.5 * (X + X.T))
        except np.linalg.LinAlgError:
            return False
        scale = max(1.0, np.linalg.norm(X, ord=2))
        if np.min(w) < -self.tol * scale:
            return False
        # Check optimality by comparing to computed projection
        X_proj = self.solve(A)
        denom = max(1.0, np.linalg.norm(X_proj, ord='fro'),
                    np.linalg.norm(A, ord='fro'))
        return np.linalg.norm(X - X_proj, ord='fro') <= self.tol * denom
