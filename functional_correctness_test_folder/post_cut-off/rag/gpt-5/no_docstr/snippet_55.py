import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def _to_matrix(self, problem):
        A = problem.get('A', None)
        if A is None:
            A = problem.get('matrix', None)
        if A is None:
            A = problem.get('data', None)
        if A is None:
            raise ValueError(
                "Problem must contain key 'A' (or 'matrix'/'data').")
        A = np.asarray(A, dtype=np.complex128)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError('Matrix A must be a square 2D array.')
        return A

    def _normalize_vector(self, v, zero_tol=1e-14):
        v = np.asarray(v, dtype=np.complex128)
        nrm = np.linalg.norm(v)
        if nrm == 0:
            return v
        v = v / nrm
        nz = np.flatnonzero(np.abs(v) > zero_tol)
        if nz.size > 0:
            k = nz[0]
            phase = np.angle(v[k])
            v = v * np.exp(-1j * phase)
            if v[k].real < 0:
                v = -v
        return v

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        A = self._to_matrix(problem)
        eigvals, eigvecs = np.linalg.eig(A)
        # eigvecs are column vectors; convert to list of vectors and normalize
        vectors = []
        for i in range(eigvecs.shape[1]):
            v = eigvecs[:, i]
            v = self._normalize_vector(v)
            vectors.append([complex(x) for x in v.tolist()])
        values = [complex(x) for x in eigvals.tolist()]
        return {
            'eigenvalues': values,
            'eigenvectors': vectors,
            'normalized': True,
            'method': 'numpy.linalg.eig',
            'shape': A.shape
        }

    def _extract_vectors_and_values(self, solution, n, A):
        vectors = None
        values = None

        if isinstance(solution, dict):
            if 'eigenvectors' in solution:
                arr = np.asarray(solution['eigenvectors'], dtype=np.complex128)
                if arr.ndim == 1:
                    arr = arr[None, :]
                # Determine orientation
                if arr.shape[1] == n:
                    # list-of-vectors -> shape (k, n)
                    vectors = [arr[i, :].copy() for i in range(arr.shape[0])]
                elif arr.shape[0] == n:
                    # columns are vectors -> shape (n, k)
                    vectors = [arr[:, i].copy() for i in range(arr.shape[1])]
                else:
                    return None, None
            elif 'vectors' in solution:
                arr = np.asarray(solution['vectors'], dtype=np.complex128)
                if arr.ndim == 1:
                    arr = arr[None, :]
                if arr.shape[1] == n:
                    vectors = [arr[i, :].copy() for i in range(arr.shape[0])]
                elif arr.shape[0] == n:
                    vectors = [arr[:, i].copy() for i in range(arr.shape[1])]
                else:
                    return None, None

            if 'eigenvalues' in solution:
                values = [complex(x) for x in solution['eigenvalues']]
            elif 'values' in solution:
                values = [complex(x) for x in solution['values']]
            elif 'eigenpairs' in solution and isinstance(solution['eigenpairs'], (list, tuple)):
                pairs = solution['eigenpairs']
                vectors = []
                values = []
                for p in pairs:
                    if isinstance(p, dict):
                        val = p.get('eigenvalue', p.get('value', None))
                        vec = p.get('eigenvector', p.get('vector', None))
                    else:
                        # tuple-like (value, vector)
                        if len(p) != 2:
                            return None, None
                        val, vec = p
                    if val is None or vec is None:
                        return None, None
                    values.append(complex(val))
                    vec = np.asarray(vec, dtype=np.complex128)
                    if vec.ndim != 1 or vec.size != n:
                        return None, None
                    vectors.append(vec.copy())
        else:
            arr = np.asarray(solution, dtype=np.complex128)
            if arr.ndim == 1:
                arr = arr[None, :]
            if arr.shape[1] == n:
                vectors = [arr[i, :].copy() for i in range(arr.shape[0])]
            elif arr.shape[0] == n:
                vectors = [arr[:, i].copy() for i in range(arr.shape[1])]
            else:
                return None, None

        if vectors is None:
            return None, None

        if values is None:
            # Compute Rayleigh quotient for each vector
            values = []
            for v in vectors:
                denom = np.vdot(v, v)
                if np.abs(denom) < 1e-14:
                    return None, None
                lam = np.vdot(v, A @ v) / denom
                values.append(complex(lam))

        if len(values) != len(vectors):
            return None, None

        return vectors, values

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
            A = self._to_matrix(problem)
        except Exception:
            return False

        n = A.shape[0]
        vectors, values = self._extract_vectors_and_values(solution, n, A)
        if vectors is None or values is None:
            return False
        if len(vectors) == 0:
            return False

        rtol = 1e-6
        atol = 1e-8

        for v, lam in zip(vectors, values):
            v = np.asarray(v, dtype=np.complex128)
            if v.ndim != 1 or v.size != n:
                return False
            if np.linalg.norm(v) == 0:
                return False
            Av = A @ v
            rhs = lam * v
            if not np.allclose(Av, rhs, rtol=rtol, atol=atol):
                # Use a relative residual as a fallback check
                denom = np.linalg.norm(A) * np.linalg.norm(v) + 1e-12
                resid = np.linalg.norm(Av - rhs) / denom
                if resid > 1e-6:
                    return False

        return True
