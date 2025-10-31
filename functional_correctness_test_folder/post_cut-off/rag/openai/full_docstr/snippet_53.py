
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
                         - "points": list of (x, y) tuples (source points)
                         - "targets": list of (x', y') tuples (target points)
        Returns:
            The solution in the format expected by the task:
                {
                    "matrix": [[a, b], [c, d]],
                    "translation": [tx, ty]
                }
        '''
        # Validate input
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary.")
        points = problem.get("points")
        targets = problem.get("targets")
        if points is None or targets is None:
            raise ValueError(
                "Problem must contain 'points' and 'targets' keys.")
        if len(points) != len(targets):
            raise ValueError("Number of points and targets must match.")
        n = len(points)
        if n == 0:
            # Return identity transform
            return {"matrix": [[1.0, 0.0], [0.0, 1.0]], "translation": [0.0, 0.0]}

        # Build linear system M * params = v
        # params = [a, b, c, d, tx, ty]
        M = np.zeros((2 * n, 6), dtype=float)
        v = np.zeros(2 * n, dtype=float)
        for i, ((x, y), (xp, yp)) in enumerate(zip(points, targets)):
            M[2 * i] = [x, y, 0, 0, 1, 0]
            M[2 * i + 1] = [0, 0, x, y, 0, 1]
            v[2 * i] = xp
            v[2 * i + 1] = yp

        # Solve least squares
        params, *_ = np.linalg.lstsq(M, v, rcond=None)
        a, b, c, d, tx, ty = params
        solution = {
            "matrix": [[float(a), float(b)], [float(c), float(d)]],
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
        # Basic validation
        if not isinstance(solution, dict):
            return False
        matrix = solution.get("matrix")
        translation = solution.get("translation")
        if matrix is None or translation is None:
            return False
        if not (isinstance(matrix, (list, tuple)) and len(matrix) == 2 and
                all(isinstance(row, (list, tuple)) and len(row) == 2 for row in matrix)):
            return False
        if not (isinstance(translation, (list, tuple)) and len(translation) == 2):
            return False

        # Extract problem data
        points = problem.get("points")
        targets = problem.get("targets")
        if points is None or targets is None or len(points) != len(targets):
            return False

        a, b = matrix[0]
        c, d = matrix[1]
        tx, ty = translation

        # Tolerance
        tol = 1e-6

        for (x, y), (xp, yp) in zip(points, targets):
            x_pred = a * x + b * y + tx
            y_pred = c * x + d * y + ty
            if not (abs(x_pred - xp) <= tol and abs(y_pred - yp) <= tol):
                return False
        return True
