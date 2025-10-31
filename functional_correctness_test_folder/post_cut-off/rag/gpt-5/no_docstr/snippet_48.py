import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def _extract_matrix(self, problem):
        for key in ('matrix', 'A', 'M', 'mat'):
            if key in problem:
                return np.asarray(problem[key], dtype=complex)
        raise ValueError(
            "Problem does not contain a matrix under keys: 'matrix', 'A', 'M', or 'mat'.")

    def _is_hermitian(self, A, tol):
        return np.allclose(A, A.conj().T, atol=tol, rtol=0)

    def _canonicalize_vector(self, v, zero_tol=1e-14):
        norm = np.linalg.norm(v)
        if norm < zero_tol:
            return v
        v = v / norm
        idx = np.argmax(np.abs(v))
        if np.abs(v[idx]) > zero_tol:
            phase = np.exp(-1j * np.angle(v[idx]))
            v = v * phase
            # Ensure positive real if possible
            if np.isclose(v[idx].imag, 0.0, atol=zero_tol) and v[idx].real < 0:
                v = -v
        return v

    def _round_complex_array(self, arr, digits=None):
        if digits is None:
            return arr
        out = np.empty_like(arr, dtype=complex)
        it = np.nditer(arr, flags=['multi_index'])
        for x in it:
            z = x.item()
            out[it.multi_index] = complex(
                round(z.real, digits), round(z.imag, digits))
        return out

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        A = self._extract_matrix(problem)
        tol = problem.get('hermitian_tol', 1e-10)
        precision = problem.get('precision', problem.get(
            'round', problem.get('decimals', None)))

        use_eigh = bool(problem.get('hermitian', False))
        if not use_eigh:
            use_eigh = self._is_hermitian(A, tol)

        if use_eigh:
            vals, vecs = np.linalg.eigh(A)
        else:
            vals, vecs = np.linalg.eig(A)

        order = np.lexsort((np.imag(vals), np.real(vals)))
        vals = vals[order]
        vecs = vecs[:, order]

        # Canonicalize eigenvectors
        for i in range(vecs.shape[1]):
            vecs[:, i] = self._canonicalize_vector(vecs[:, i])

        if precision is not None:
            try:
                digits = int(precision)
            except Exception:
                digits = None
            if digits is not None:
                vecs = self._round_complex_array(vecs, digits)

        eigenvectors_list = [
            [complex(c) for c in vecs[:, i].tolist()] for i in range(vecs.shape[1])]

        return {'eigenvectors': eigenvectors_list}

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
            A = self._extract_matrix(problem)
        except Exception:
            return False

        # Accept either dict with 'eigenvectors' or a raw list/ndarray of vectors
        if isinstance(solution, dict):
            if 'eigenvectors' not in solution:
                return False
            evs = solution['eigenvectors']
        else:
            evs = solution

        try:
            V = np.asarray(evs, dtype=complex)
        except Exception:
            return False

        if V.ndim == 1:
            V = V[:, None]
        elif V.ndim == 2:
            # assume list of vectors, shape should be (k, n) or (n, k). Try to infer:
            # Prefer interpretting as list of vectors of length n => shape (k, n)
            # If rows have length != n, try transpose.
            if V.shape[1] == A.shape[0]:
                V = V.T  # make columns vectors
            elif V.shape[0] == A.shape[0]:
                pass  # already columns
            else:
                return False
        else:
            return False

        n = A.shape[0]
        if V.shape[0] != n:
            return False

        atol = problem.get('atol', 1e-6)
        rtol = problem.get('rtol', 1e-6)

        for i in range(V.shape[1]):
            v = V[:, i]
            if not np.any(np.abs(v) > atol):
                return False
            Av = A @ v
            denom = np.vdot(v, v)
            if np.abs(denom) < atol:
                return False
            lam = np.vdot(v, Av) / denom
            residual = np.linalg.norm(Av - lam * v)
            if residual > atol + rtol * np.linalg.norm(Av):
                return False

        return True
