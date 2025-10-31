class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
                     Expected keys:
                       - 'matrix': square matrix (list of lists or numpy array)
                       - optional 'symmetric': bool, if True, assumes input is symmetric
                       - optional 'tol': numerical tolerance (float)
        Returns:
            The projected PSD matrix as a list of lists under key 'projected_matrix'
        '''
        import numpy as np

        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary.")

        if 'matrix' not in problem:
            raise KeyError("Problem dictionary must contain key 'matrix'.")

        A = np.array(problem['matrix'], dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix must be a square 2D array.")

        tol = float(problem.get('tol', 1e-10))
        symmetric = bool(problem.get('symmetric', False))

        # Symmetrize unless told it's already symmetric
        if symmetric:
            S = A
        else:
            S = 0.5 * (A + A.T)

        # Eigen-decomposition
        w, Q = np.linalg.eigh(S)
        w_clipped = np.clip(w, 0.0, None)

        # Reconstruct projected matrix
        X = (Q * w_clipped) @ Q.T
        # Enforce symmetry numerically
        X = 0.5 * (X + X.T)

        return {'projected_matrix': X.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution (dict with 'projected_matrix' or a matrix)
        Returns:
            True if the solution is valid, False otherwise
        '''
        import numpy as np

        if not isinstance(problem, dict) or 'matrix' not in problem:
            return False

        tol = float(problem.get('tol', 1e-10))
        A = np.array(problem['matrix'], dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False

        # Extract solution matrix
        if isinstance(solution, dict) and 'projected_matrix' in solution:
            X = np.array(solution['projected_matrix'], dtype=float)
        else:
            X = np.array(solution, dtype=float)

        if X.ndim != 2 or X.shape != A.shape:
            return False

        # Check symmetry
        if not np.allclose(X, X.T, atol=max(tol, 1e-12), rtol=0):
            return False

        # Check positive semidefiniteness
        try:
            w = np.linalg.eigvalsh(X)
        except np.linalg.LinAlgError:
            return False

        if np.min(w) < -10 * tol:
            return False

        return True
