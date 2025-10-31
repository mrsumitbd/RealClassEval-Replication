import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def _combine_real_imag(self, real, imag):
        real = np.asarray(real, dtype=float)
        imag = np.asarray(imag, dtype=float)
        if real.shape != imag.shape:
            raise ValueError(
                "Real and imaginary parts must have the same shape.")
        return real + 1j * imag

    def _parse_matrix(self, problem):
        # Accept various keys and formats
        if 'A' in problem:
            A = problem['A']
        elif 'matrix' in problem:
            A = problem['matrix']
        elif 'real' in problem and 'imag' in problem:
            return self._combine_real_imag(problem['real'], problem['imag'])
        elif 'matrix_real' in problem and 'matrix_imag' in problem:
            return self._combine_real_imag(problem['matrix_real'], problem['matrix_imag'])
        elif 'A_real' in problem and 'A_imag' in problem:
            return self._combine_real_imag(problem['A_real'], problem['A_imag'])
        else:
            raise ValueError("Problem must contain a complex matrix under keys like 'A' or 'matrix', "
                             "or provide 'real' and 'imag' parts.")

        # If A is a dict with real/imag
        if isinstance(A, dict):
            if 'real' in A and 'imag' in A:
                return self._combine_real_imag(A['real'], A['imag'])
            else:
                raise ValueError(
                    "Matrix dict must contain 'real' and 'imag' keys.")

        A = np.asarray(A)
        # If dtype is not complex, accept as complex if possible
        if not np.issubdtype(A.dtype, np.complexfloating):
            A = A.astype(np.complex128)
        return A

    def _normalize_vector(self, v, phase_fix=True):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        v = v / norm
        if phase_fix:
            idx = np.argmax(np.abs(v))
            if np.abs(v[idx]) > 0:
                phase = np.angle(v[idx])
                v = v * np.exp(-1j * phase)
                # Ensure non-negative real part on the anchor component
                if np.real(v[idx]) < 0:
                    v = -v
        return v

    def _sort_eigenpairs(self, w, V):
        # Sort eigenpairs by (real, imag) for deterministic ordering
        idx = np.lexsort((np.imag(w), np.real(w)))
        return w[idx], V[:, idx]

    def _format_solution(self, w, V, problem):
        # Determine output preference
        ret = problem.get('return', problem.get('output', 'both'))
        eigenvalues_list = [complex(val) for val in w]
        # Return eigenvectors as list of column vectors (each a python list)
        eigenvectors_list = [list(V[:, i]) for i in range(V.shape[1])]

        if ret == 'eigenvectors':
            return {'eigenvectors': eigenvectors_list}
        elif ret == 'eigenvalues':
            return {'eigenvalues': eigenvalues_list}
        else:
            return {'eigenvalues': eigenvalues_list, 'eigenvectors': eigenvectors_list}

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        A = self._parse_matrix(problem)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix must be square.")
        # Compute eigenvalues and eigenvectors
        w, V = np.linalg.eig(A.astype(np.complex128))

        # Normalize eigenvectors and fix phase for determinism
        V = np.asarray([self._normalize_vector(V[:, i])
                       for i in range(V.shape[1])], dtype=np.complex128).T

        # Sort eigenpairs deterministically
        w, V = self._sort_eigenpairs(w, V)

        return self._format_solution(w, V, problem)

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
            A = self._parse_matrix(problem)
            n = A.shape[0]

            # Extract eigenvectors and eigenvalues from solution
            w = None
            V_list = None

            if isinstance(solution, dict):
                if 'eigenvectors' in solution:
                    V_list = solution['eigenvectors']
                elif 'vectors' in solution:
                    V_list = solution['vectors']
                elif 'V' in solution:
                    V_list = solution['V']

                if 'eigenvalues' in solution:
                    w = solution['eigenvalues']
                elif 'values' in solution:
                    w = solution['values']
                elif 'w' in solution:
                    w = solution['w']
            else:
                # If solution is directly a list of vectors
                V_list = solution

            if V_list is None:
                return False

            V = np.asarray(V_list, dtype=np.complex128)
            # Accept either list of column vectors shape (k, n) or matrix (n, k)
            if V.ndim == 1:
                V = V.reshape(-1, 1)
            # If shape is (k, n) where k != n, guess orientation based on matching n
            if V.shape[0] != n and V.shape[1] == n:
                V = V.T
            if V.shape[0] != n:
                return False

            # Prepare eigenvalues if provided
            if w is not None:
                w = np.asarray(w, dtype=np.complex128)
                if w.ndim != 1:
                    return False
                if w.size != V.shape[1]:
                    return False

            # Validate each vector
            tol = 1e-6
            if 'tolerance' in problem:
                try:
                    tol = float(problem['tolerance'])
                except Exception:
                    pass

            k = V.shape[1]
            if k == 0:
                return False

            for i in range(k):
                v = V[:, i]
                nv = np.linalg.norm(v)
                if not np.isfinite(nv) or nv == 0:
                    return False
                Av = A @ v
                if w is not None:
                    lam = w[i]
                else:
                    # Rayleigh quotient
                    lam = (np.vdot(v, Av) / np.vdot(v, v))
                residual = Av - lam * v
                denom = np.linalg.norm(A, ord=2) * nv + 1e-12
                if np.linalg.norm(residual) > max(tol, tol * denom):
                    return False

            return True
        except Exception:
            return False
