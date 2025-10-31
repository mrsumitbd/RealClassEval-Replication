
import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
                     Expected keys:
                         - "points": list of [x, y] source points
                         - "targets": list of [x', y'] target points
        Returns:
            The solution in the format expected by the task:
                {
                    "matrix": [[a11, a12], [a21, a22]],
                    "translation": [tx, ty]
                }
        '''
        points = np.asarray(problem.get("points", []), dtype=float)
        targets = np.asarray(problem.get("targets", []), dtype=float)

        if points.shape != targets.shape or points.ndim != 2 or points.shape[1] != 2:
            raise ValueError(
                "Problem must contain matching lists of 2D points and targets.")

        n = points.shape[0]
        # Build design matrix X (2n x 6) and target vector Y (2n,)
        X = np.zeros((2 * n, 6), dtype=float)
        Y = np.zeros(2 * n, dtype=float)

        for i in range(n):
            x, y = points[i]
            xp, yp = targets[i]
            # Row for x'
            X[2 * i] = [x, y, 0, 0, 1, 0]
            Y[2 * i] = xp
            # Row for y'
            X[2 * i + 1] = [0, 0, x, y, 0, 1]
            Y[2 * i + 1] = yp

        # Solve least squares
        coeffs, *_ = np.linalg.lstsq(X, Y, rcond=None)
        a11, a12, a21, a22, tx, ty = coeffs

        solution = {
            "matrix": [[float(a11), float(a12)], [float(a21), float(a22)]],
            "translation": [float(tx), float(ty)]
        }
        return solution

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
            points = np.asarray(problem.get("points", []), dtype=float)
            targets = np.asarray(problem.get("targets", []), dtype=float)
            if points.shape != targets.shape or points.ndim != 2 or points.shape[1] != 2:
                return False

            matrix = np.asarray(solution.get("matrix", []), dtype=float)
            translation = np.asarray(solution.get(
                "translation", []), dtype=float)

            if matrix.shape != (2, 2) or translation.shape != (2,):
                return False

            # Apply transformation
            transformed = points @ matrix.T + translation
            # Check within tolerance
            return np.allclose(transformed, targets, atol=1e-6, rtol=0)
        except Exception:
            return False
