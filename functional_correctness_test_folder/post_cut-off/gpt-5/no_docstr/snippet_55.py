import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        self.rtol = 1e-7
        self.atol = 1e-8

    def _as_square_matrix(self, problem):
        A = np.asarray(problem, dtype=complex)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Problem must be a square matrix.")
        return A

    def _normalize_vector(self, v):
        v = np.asarray(v, dtype=complex).reshape(-1)
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        v = v / norm
        idx = np.argmax(np.abs(v))
        if np.abs(v[idx]) > 0:
            phase = v[idx] / np.abs(v[idx])
            v = v / phase
        return v

    def solve(self, problem):
        A = self._as_square_matrix(problem)
        w, V = np.linalg.eig(A)
        vectors = []
        for i in range(V.shape[1]):
            vec = self._normalize_vector(V[:, i])
            vectors.append(vec.tolist())
        return {"eigenvalues": w.tolist(), "eigenvectors": vectors}

    def is_solution(self, problem, solution):
        try:
            A = self._as_square_matrix(problem)
        except Exception:
            return False
        if not isinstance(solution, dict):
            return False
        if "eigenvalues" not in solution or "eigenvectors" not in solution:
            return False
        vals = np.asarray(solution["eigenvalues"], dtype=complex)
        vecs = solution["eigenvectors"]
        if vals.ndim != 1:
            return False
        if not isinstance(vecs, (list, tuple)) or len(vecs) != len(vals):
            return False
        n = A.shape[0]
        for lam, v in zip(vals, vecs):
            v = np.asarray(v, dtype=complex).reshape(-1)
            if v.ndim != 1 or v.shape[0] != n:
                return False
            if np.linalg.norm(v) == 0:
                return False
            lhs = A @ v
            rhs = lam * v
            if not np.allclose(lhs, rhs, rtol=self.rtol, atol=self.atol):
                return False
        return True
