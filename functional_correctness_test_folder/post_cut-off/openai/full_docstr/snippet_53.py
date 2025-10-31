
import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
                     Expected keys:
                         - "points": list of (x, y) tuples (source points)
                         - "transformed": list of (x', y') tuples (target points)
        Returns:
            The solution in the format:
                {
                    "matrix": [[a11, a12], [a21, a22]],
                    "translation": [tx, ty]
                }
            or None if the problem cannot be solved.
        '''
        pts = problem.get("points")
        tgt = problem.get("transformed")

        if pts is None or tgt is None:
            return None

        if len(pts) != len(tgt) or len(pts) < 3:
            # Need at least 3 non-collinear points for a unique affine transform
            return None

        n = len(pts)
        # Build design matrix M and target vector b
        M = np.zeros((2 * n, 6))
        b = np.zeros((2 * n,))

        for i, ((x, y), (xp, yp)) in enumerate(zip(pts, tgt)):
            M[2 * i] = [x, y, 0, 0, 1, 0]
            M[2 * i + 1] = [0, 0, x, y, 0, 1]
            b[2 * i] = xp
            b[2 * i + 1] = yp

        # Solve least squares
        try:
            coeffs, *_ = np.linalg.lstsq(M, b, rcond=None)
        except Exception:
            return None

        a11, a12, a21, a22, tx, ty = coeffs
        return {
            "matrix": [[float(a11), float(a12)], [float(a21), float(a22)]],
            "translation": [float(tx), float(ty)]
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
        if solution is None:
            return False

        matrix = solution.get("matrix")
        translation = solution.get("translation")

        if matrix is None or translation is None:
            return False

        try:
            a11, a12 = matrix[0]
            a21, a22 = matrix[1]
            tx, ty = translation
        except Exception:
            return False

        pts = problem.get("points")
        tgt = problem.get("transformed")

        if pts is None or tgt is None or len(pts) != len(tgt):
            return False

        tol = 1e-6
        for (x, y), (xp, yp) in zip(pts, tgt):
            xp_pred = a11 * x + a12 * y + tx
            yp_pred = a21 * x + a22 * y + ty
            if abs(xp_pred - xp) > tol or abs(yp_pred - yp) > tol:
                return False

        return True
