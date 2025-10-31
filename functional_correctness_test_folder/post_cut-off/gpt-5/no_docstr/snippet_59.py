import numpy as np


class PSDConeProjection:

    def __init__(self, atol: float = 1e-8, rtol: float = 1e-7):
        self.atol = atol
        self.rtol = rtol

    def solve(self, problem):
        A = np.asarray(problem, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input must be a square 2D array.")
        # Symmetrize to handle numerical asymmetry
        S = 0.5 * (A + A.T)
        # Eigen-decomposition
        eigvals, eigvecs = np.linalg.eigh(S)
        # Clip eigenvalues to enforce PSD
        eigvals_clipped = np.maximum(eigvals, 0.0)
        # Reconstruct PSD projection
        S_psd = (eigvecs * eigvals_clipped) @ eigvecs.T
        # Ensure symmetry
        S_psd = 0.5 * (S_psd + S_psd.T)
        return S_psd

    def is_solution(self, problem, solution):
        A = np.asarray(problem, dtype=float)
        X = np.asarray(solution, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        if X.shape != A.shape:
            return False
        # Check symmetry of solution
        if not np.allclose(X, X.T, atol=self.atol, rtol=self.rtol):
            return False
        # Check PSD (eigenvalues >= -tol)
        try:
            w = np.linalg.eigvalsh(0.5 * (X + X.T))
        except np.linalg.LinAlgError:
            return False
        if np.min(w) < -10 * self.atol:
            return False
        # Check optimality by recomputing projection and comparing
        X_star = self.solve(A)
        return np.allclose(X, X_star, atol=10 * self.atol, rtol=self.rtol)
