class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, tol=1e-6):
        '''Initialize the EigenvectorsComplex.'''
        self.tol = tol

    def _extract_matrix(self, problem):
        import numpy as np
        A = None
        if isinstance(problem, dict):
            for key in ['A', 'matrix', 'input', 'M', 'data']:
                if key in problem:
                    A = problem[key]
                    break
        elif hasattr(problem, '__array__') or hasattr(problem, '__iter__'):
            A = problem
        if A is None:
            raise ValueError("Problem does not contain a matrix.")
        A = np.asarray(A, dtype=np.complex128)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix must be square 2D.")
        return A

    def _parse_solution(self, solution):
        import numpy as np
        eigvals = None
        eigvecs = None
        if isinstance(solution, dict):
            if 'eigenvalues' in solution:
                eigvals = np.asarray(
                    solution['eigenvalues'], dtype=np.complex128)
            if 'eigenvectors' in solution:
                eigvecs = np.asarray(
                    solution['eigenvectors'], dtype=np.complex128)
        elif isinstance(solution, (list, tuple)) and len(solution) == 2:
            eigvals = np.asarray(
                solution[0], dtype=np.complex128) if solution[0] is not None else None
            eigvecs = np.asarray(
                solution[1], dtype=np.complex128) if solution[1] is not None else None
        else:
            # maybe only eigenvectors provided
            try:
                arr = np.asarray(solution, dtype=np.complex128)
                if arr.ndim >= 2:
                    eigvecs = arr
                else:
                    eigvecs = arr.reshape(-1, 1)
            except Exception:
                pass
        return eigvals, eigvecs

    def solve(self, problem):
        import numpy as np
        A = self._extract_matrix(problem)
        w, V = np.linalg.eig(A)
        return {'eigenvalues': w.tolist(), 'eigenvectors': V.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        import numpy as np
        try:
            A = self._extract_matrix(problem)
        except Exception:
            return False

        eigvals, eigvecs = self._parse_solution(solution)
        n = A.shape[0]

        if eigvecs is None and eigvals is None:
            return False

        if eigvecs is not None:
            eigvecs = np.asarray(eigvecs, dtype=np.complex128)
            if eigvecs.ndim == 1:
                eigvecs = eigvecs.reshape(-1, 1)
            # Try columns first; if not matching size, maybe rows are vectors
            if eigvecs.shape[0] != n and eigvecs.shape[1] == n:
                eigvecs = eigvecs.T
            if eigvecs.shape[0] != n:
                return False

        if eigvals is not None:
            eigvals = np.asarray(eigvals, dtype=np.complex128).reshape(-1)

        # If eigenvectors not provided but eigenvalues are, we can verify by recomputing eigendecomposition and matching sets
        if eigvecs is None and eigvals is not None:
            try:
                w, _ = np.linalg.eig(A)
            except Exception:
                return False
            # Compare multisets within tolerance
            w_list = list(w)
            vals = list(eigvals)
            used = [False] * len(w_list)
            for val in vals:
                found = False
                for i, ww in enumerate(w_list):
                    if not used[i] and np.isclose(val, ww, atol=max(self.tol, self.tol * max(1.0, abs(ww))), rtol=1e-6):
                        used[i] = True
                        found = True
                        break
                if not found:
                    return False
            return True

        # If eigenvectors provided, validate Av = lambda v.
        if eigvecs is None:
            return False

        k = eigvecs.shape[1]
        if eigvals is not None and eigvals.shape[0] != k:
            # lengths mismatch; allow if eigvals is n and eigvecs subset, or vice versa
            # We will proceed using min length
            k = min(k, eigvals.shape[0])
            eigvecs = eigvecs[:, :k]
            eigvals = eigvals[:k]

        # If no eigenvalues provided, infer each by Rayleigh quotient
        if eigvals is None:
            eigvals = np.empty(k, dtype=np.complex128)
            for j in range(k):
                v = eigvecs[:, j]
                nv2 = np.vdot(v, v)
                if abs(nv2) < 1e-14:
                    return False
                eigvals[j] = np.vdot(v, A @ v) / nv2

        # Validate each vector
        A_norm = np.linalg.norm(A, ord=np.inf)
        for j in range(k):
            v = eigvecs[:, j]
            lv = eigvals[j]
            nv = np.linalg.norm(v)
            if nv < 1e-12:
                return False
            residual = A @ v - lv * v
            res_norm = np.linalg.norm(residual)
            tol = max(self.tol, self.tol * (1.0 + A_norm) * nv)
            if res_norm > tol:
                # Try if vectors are rows
                if eigvecs.shape[0] == k and eigvecs.shape[1] == n:
                    Vt = eigvecs.T
                    ok_all = True
                    for jj in range(Vt.shape[1]):
                        v2 = Vt[:, jj]
                        if np.linalg.norm(v2) < 1e-12:
                            ok_all = False
                            break
                        lv2 = eigvals[jj] if jj < len(eigvals) else np.vdot(
                            v2, A @ v2) / np.vdot(v2, v2)
                        r2 = A @ v2 - lv2 * v2
                        if np.linalg.norm(r2) > max(self.tol, self.tol * (1.0 + A_norm) * np.linalg.norm(v2)):
                            ok_all = False
                            break
                    return ok_all
                return False
        return True
