import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        pass

    def _to_complex(self, x):
        if isinstance(x, complex) or isinstance(x, (int, float, np.number)):
            return complex(x)
        if isinstance(x, str):
            return complex(x.replace('i', 'j'))
        if isinstance(x, dict):
            re = x.get('re', 0.0)
            im = x.get('im', 0.0)
            return complex(float(re), float(im))
        if isinstance(x, (list, tuple)) and len(x) == 2:
            return complex(float(x[0]), float(x[1]))
        raise ValueError("Unsupported complex format")

    def _from_complex(self, z):
        return [float(np.real(z)), float(np.imag(z))]

    def _parse_matrix(self, A):
        return np.array([[self._to_complex(v) for v in row] for row in A], dtype=complex)

    def _parse_vector(self, v):
        return np.array([self._to_complex(x) for x in v], dtype=complex)

    def _encode_vector(self, v):
        return [self._from_complex(x) for x in v]

    def _eig(self, A):
        w, V = np.linalg.eig(A)
        return w, V

    def _select_vectors_for_eigenvalue(self, A, eigvals, eigvecs, target, tol):
        indices = [i for i, lam in enumerate(eigvals) if np.abs(
            lam - target) <= max(tol, tol * max(1.0, np.abs(lam), np.abs(target)))]
        selected = []
        for i in indices:
            v = eigvecs[:, i]
            if np.linalg.norm(v) == 0:
                continue
            selected.append(v)
        # Attempt to augment basis in case of defective/near-duplicate eigenvalues using nullspace of (A - λI)
        if not selected:
            M = A - target * np.eye(A.shape[0], dtype=complex)
            # SVD-based nullspace
            U, S, VT = np.linalg.svd(M)
            # singular values close to 0
            mask = S <= tol * max(1.0, np.linalg.norm(A), 1.0)
            # If any singular values are ~0, take corresponding right-singular vectors
            if np.any(mask):
                for j, small in enumerate(mask):
                    if small:
                        v = VT[-(len(S)-j), :].conj()
                        if np.linalg.norm(v) != 0:
                            selected.append(v)
        # Normalize for consistency
        normed = []
        for v in selected:
            n = np.linalg.norm(v)
            if n == 0:
                continue
            # phase normalization: make first nonzero element real-positive
            v = v / n
            for k, val in enumerate(v):
                if np.abs(val) > 1e-12:
                    phase = np.exp(-1j * np.angle(val))
                    v = v * phase
                    break
            normed.append(v)
        return normed

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary")
        if 'A' not in problem:
            raise ValueError("Problem missing key 'A'")
        tol = float(problem.get('tol', 1e-8))
        A = self._parse_matrix(problem['A'])
        if 'eigenvalue' in problem:
            lam = self._to_complex(problem['eigenvalue'])
            w, V = self._eig(A)
            vecs = self._select_vectors_for_eigenvalue(A, w, V, lam, tol)
            return [self._encode_vector(v.tolist()) for v in vecs]
        else:
            w, V = self._eig(A)
            eigenvalues = [self._from_complex(val) for val in w.tolist()]
            eigenvectors = []
            for i in range(V.shape[1]):
                v = V[:, i]
                # Normalize similarly as in selection
                n = np.linalg.norm(v)
                if n != 0:
                    v = v / n
                    for k, val in enumerate(v):
                        if np.abs(val) > 1e-12:
                            phase = np.exp(-1j * np.angle(val))
                            v = v * phase
                            break
                eigenvectors.append(self._encode_vector(v.tolist()))
            return {'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}

    def is_solution(self, problem, solution):
        try:
            tol = float(problem.get('tol', 1e-6))
            A = self._parse_matrix(problem['A'])
            n = A.shape[0]
            if 'eigenvalue' in problem:
                lam = self._to_complex(problem['eigenvalue'])
                vecs = solution
                if isinstance(solution, dict) and 'eigenvectors' in solution:
                    vecs = solution['eigenvectors']
                if not isinstance(vecs, (list, tuple)):
                    return False
                if len(vecs) == 0:
                    # Accept empty if no eigenvectors exist numerically (rare), but usually expect at least one
                    # We'll check numerically if λ is indeed an eigenvalue
                    w, _ = np.linalg.eig(A)
                    return np.min(np.abs(w - lam)) <= tol * max(1.0, np.linalg.norm(A))
                for v_enc in vecs:
                    v = self._parse_vector(v_enc)
                    if v.shape != (n,):
                        return False
                    nv = np.linalg.norm(v)
                    if not np.isfinite(nv) or nv == 0:
                        return False
                    residual = A.dot(v) - lam * v
                    if np.linalg.norm(residual) > tol * (1.0 + np.linalg.norm(v)):
                        return False
                return True
            else:
                if not isinstance(solution, dict):
                    return False
                if 'eigenvectors' not in solution or 'eigenvalues' not in solution:
                    return False
                vals = solution['eigenvalues']
                vecs = solution['eigenvectors']
                if not (isinstance(vals, (list, tuple)) and isinstance(vecs, (list, tuple))):
                    return False
                if len(vals) != len(vecs):
                    return False
                for lam_enc, v_enc in zip(vals, vecs):
                    lam = self._to_complex(lam_enc)
                    v = self._parse_vector(v_enc)
                    if v.shape != (n,):
                        return False
                    nv = np.linalg.norm(v)
                    if not np.isfinite(nv) or nv == 0:
                        return False
                    residual = A.dot(v) - lam * v
                    if np.linalg.norm(residual) > tol * (1.0 + np.linalg.norm(v)):
                        return False
                return True
        except Exception:
            return False
