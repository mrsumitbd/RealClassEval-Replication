
import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.tol = 1e-6

    def solve(self, problem):
        """
        Compute an affine transformation that maps the source points to the target points.
        The transformation is represented as a 2x2 matrix A and a translation vector t,
        such that for each source point p:  A @ p + t ≈ target.

        Parameters
        ----------
        problem : dict
            Must contain 'src' and 'dst' keys, each mapping to an iterable of
            (x, y) tuples or 2-element arrays. The two lists must have the same
            length and contain at least 3 non-collinear points.

        Returns
        -------
        dict or None
            If a solution is found, returns a dictionary with keys:
                'A' : 2x2 numpy array
                't' : 2-element numpy array
            If the problem is ill-posed or insufficient data, returns None.
        """
        # Validate input
        if not isinstance(problem, dict):
            return None
        if 'src' not in problem or 'dst' not in problem:
            return None

        src = np.asarray(problem['src'], dtype=float)
        dst = np.asarray(problem['dst'], dtype=float)

        if src.ndim != 2 or dst.ndim != 2 or src.shape[1] != 2 or dst.shape[1] != 2:
            return None
        if src.shape[0] != dst.shape[0] or src.shape[0] < 3:
            return None

        # Build linear system: [x y 1 0 0 0; 0 0 0 x y 1] * [a11 a12 a21 a22 tx ty]^T = [dx dy]^T
        n = src.shape[0]
        X = np.zeros((2 * n, 6))
        Y = np.zeros((2 * n, 1))
        for i in range(n):
            x, y = src[i]
            dx, dy = dst[i]
            X[2 * i] = [x, y, 0, 0, 0, 1]
            X[2 * i + 1] = [0, 0, x, y, 0, 1]
            Y[2 * i] = [dx]
            Y[2 * i + 1] = [dy]

        # Solve least squares
        try:
            coeffs, *_ = np.linalg.lstsq(X, Y, rcond=None)
        except np.linalg.LinAlgError:
            return None

        a11, a12, a21, a22, tx, ty = coeffs.ravel()
        A = np.array([[a11, a12], [a21, a22]])
        t = np.array([tx, ty])

        return {'A': A, 't': t}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if solution is None:
            return False
        if not isinstance(solution, dict):
            return False
        if 'A' not in solution or 't' not in solution:
            return False

        A = np.asarray(solution['A'], dtype=float)
        t = np.asarray(solution['t'], dtype=float)

        if A.shape != (2, 2) or t.shape != (2,):
            return False

        # Validate mapping
        src = np.asarray(problem.get('src', []), dtype=float)
        dst = np.asarray(problem.get('dst', []), dtype=float)

        if src.ndim != 2 or dst.ndim != 2 or src.shape != dst.shape:
            return False

        transformed = src @ A.T + t
        diff = np.linalg.norm(transformed - dst, axis=1)
        return np.all(diff <= self.tol)
