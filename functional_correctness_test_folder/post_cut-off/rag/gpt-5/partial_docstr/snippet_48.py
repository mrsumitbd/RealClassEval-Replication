import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def _get_matrix(self, problem):
        if isinstance(problem, dict):
            for key in ('matrix', 'A', 'mat', 'M'):
                if key in problem:
                    A = problem[key]
                    break
            else:
                raise ValueError(
                    "Problem dictionary must contain a matrix under one of keys: 'matrix', 'A', 'mat', 'M'.")
        else:
            A = problem
        A = np.asarray(A, dtype=np.complex128)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix must be a square 2D array.")
        return A

    def _normalize_vector(self, v):
        v = np.asarray(v, dtype=np.complex128).reshape(-1)
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
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        A = self._get_matrix(problem)
        if A.size == 0:
            return {'eigenvalues': [], 'eigenvectors': []}
        vals, vecs = np.linalg.eig(A)
        vectors = []
        for i in range(vecs.shape[1]):
            v = vecs[:, i]
            v = self._normalize_vector(v)
            vectors.append([complex(x) for x in v.tolist()])
        values = [complex(x) for x in vals.tolist()]
        return {'eigenvalues': values, 'eigenvectors': vectors}

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
            A = self._get_matrix(problem)
        except Exception:
            return False

        n = A.shape[0]

        # Accept several formats:
        # - dict with 'eigenvectors' and optional 'eigenvalues'
        # - list/array of vectors
        eigvecs = None
        eigvals = None
        if isinstance(solution, dict):
            if 'eigenvectors' not in solution:
                return False
            eigvecs = solution.get('eigenvectors', None)
            eigvals = solution.get('eigenvalues', None)
        else:
            eigvecs = solution

        if eigvecs is None:
            return False

        # Normalize input vectors shape
        try:
            vectors = []
            for v in eigvecs:
                vv = np.asarray(v, dtype=np.complex128).reshape(-1)
                vectors.append(vv)
        except Exception:
            return False

        if len(vectors) == 0:
            return n == 0

        # Prepare eigenvalues if provided
        if eigvals is not None:
            try:
                eigvals = [complex(x) for x in eigvals]
            except Exception:
                return False
            if len(eigvals) != len(vectors):
                return False

        # Tolerances
        atol = 1e-8
        rtol = 1e-6

        for i, v in enumerate(vectors):
            if v.shape[0] != n:
                return False
            vnorm = np.linalg.norm(v)
            if not np.isfinite(vnorm) or vnorm == 0:
                return False

            Av = A.dot(v)
            if eigvals is not None:
                lam = eigvals[i]
            else:
                denom = np.vdot(v, v)
                if denom == 0:
                    return False
                lam = np.vdot(v, Av) / denom

            residual = Av - lam * v
            rnorm = np.linalg.norm(residual)
            scale = np.linalg.norm(Av) + np.linalg.norm(lam * v) + 1.0
            if not np.isfinite(rnorm) or rnorm > atol + rtol * scale:
                return False

        return True
