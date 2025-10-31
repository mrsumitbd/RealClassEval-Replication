class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        self.atol = 1e-8
        self.rtol = 1e-6

    def _to_numpy_complex_matrix(self, A):
        import numpy as np
        if A is None:
            raise ValueError(
                "Matrix A is required in problem dictionary under key 'A' or 'matrix'.")
        arr = np.array(A, dtype=complex)
        if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
            raise ValueError("Matrix must be a square 2D array.")
        return arr

    def _complex_to_pair(self, z):
        return [float(z.real), float(z.imag)]

    def _pair_to_complex(self, v):
        # Accept complex, real, tuple/list pair
        if isinstance(v, complex):
            return v
        if isinstance(v, (int, float)):
            return complex(v, 0.0)
        if isinstance(v, (list, tuple)):
            if len(v) == 2 and all(isinstance(x, (int, float)) for x in v):
                return complex(float(v[0]), float(v[1]))
            # If it's a vector, will be handled elsewhere
        raise ValueError("Invalid complex representation.")

    def _parse_solution(self, solution):
        # Returns (eigvals: list[complex], eigvecs: 2D numpy array with shape (n, n))
        import numpy as np
        if not isinstance(solution, dict):
            raise ValueError("Solution must be a dictionary.")
        if 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            raise ValueError(
                "Solution must contain 'eigenvalues' and 'eigenvectors'.")
        eigvals_raw = solution['eigenvalues']
        eigvecs_raw = solution['eigenvectors']
        eigvals = []
        for ev in eigvals_raw:
            if isinstance(ev, (int, float, complex)):
                eigvals.append(complex(ev))
            elif isinstance(ev, (list, tuple)) and len(ev) == 2:
                eigvals.append(self._pair_to_complex(ev))
            else:
                raise ValueError("Invalid eigenvalue format.")
        # Eigenvectors expected as list of vectors (each vector length n), aligned to eigenvalues
        # Each entry can be complex or [r, i]
        if not isinstance(eigvecs_raw, (list, tuple)):
            raise ValueError("Eigenvectors must be a list.")
        if len(eigvecs_raw) != len(eigvals):
            raise ValueError(
                "Number of eigenvectors must match number of eigenvalues.")
        vectors = []
        for vec in eigvecs_raw:
            if not isinstance(vec, (list, tuple)):
                raise ValueError("Each eigenvector must be a list.")
            cv = []
            for entry in vec:
                if isinstance(entry, (int, float, complex)):
                    cv.append(complex(entry))
                elif isinstance(entry, (list, tuple)) and len(entry) == 2:
                    cv.append(self._pair_to_complex(entry))
                else:
                    raise ValueError("Invalid eigenvector entry.")
            vectors.append(cv)
        V = np.array(vectors, dtype=complex).T  # columns as eigenvectors
        return eigvals, V

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        import numpy as np
        A = problem.get('A', None)
        if A is None:
            A = problem.get('matrix', None)
        A = self._to_numpy_complex_matrix(A)
        w, V = np.linalg.eig(A)

        # Normalize eigenvectors to unit norm for determinism
        for i in range(V.shape[1]):
            norm = np.linalg.norm(V[:, i])
            if norm > 0:
                V[:, i] = V[:, i] / norm

        # Sort by eigenvalue (real, imag)
        idx = sorted(range(len(w)), key=lambda i: (
            float(w[i].real), float(w[i].imag)))
        w_sorted = np.array([w[i] for i in idx], dtype=complex)
        V_sorted = np.array([V[:, i] for i in idx], dtype=complex).T

        eigenvalues_serializable = [self._complex_to_pair(z) for z in w_sorted]
        eigenvectors_serializable = []
        for i in range(V_sorted.shape[1]):
            vec = V_sorted[:, i]
            eigenvectors_serializable.append(
                [self._complex_to_pair(z) for z in vec])

        return {
            'eigenvalues': eigenvalues_serializable,
            'eigenvectors': eigenvectors_serializable
        }

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
            A = problem.get('A', None)
            if A is None:
                A = problem.get('matrix', None)
            A = self._to_numpy_complex_matrix(A)
            n = A.shape[0]
            eigvals, V = self._parse_solution(solution)
            if len(eigvals) != n:
                return False
            if V.shape != (n, n):
                return False
            # Check A v ≈ λ v for each eigenpair
            for i in range(n):
                v = V[:, i]
                lam = eigvals[i]
                Av = A @ v
                lv = lam * v
                if not np.allclose(Av, lv, rtol=self.rtol, atol=self.atol):
                    return False
            return True
        except Exception:
            return False
