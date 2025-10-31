
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
                         - "targets": list of (x', y') tuples (destination points)
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
        if "points" not in problem or "targets" not in problem:
            raise ValueError(
                "Problem must contain 'points' and 'targets' keys.")
        points = problem["points"]
        targets = problem["targets"]
        if len(points) != len(targets):
            raise ValueError("Number of points and targets must match.")
        n = len(points)
        if n == 0:
            # Identity transform
            return {"matrix": [[1.0, 0.0], [0.0, 1.0]], "translation": [0.0, 0.0]}

        # Build linear system A * params = b
        # params = [a, b, c, d, tx, ty]
        A_rows = []
        b_vals = []
        for (x, y), (xp, yp) in zip(points, targets):
            A_rows.append([x, y, 0, 0, 1, 0])
            A_rows.append([0, 0, x, y, 0, 1])
            b_vals.append(xp)
            b_vals.append(yp)
        A = np.array(A_rows, dtype=float)
        b = np.array(b_vals, dtype=float)

        # Solve least squares (handles overdetermined systems)
        params, *_ = np.linalg.lstsq(A, b, rcond=None)
        a, b_coef, c, d, tx, ty = params
        return {
            "matrix": [[float(a), float(b_coef)], [float(c), float(d)]],
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
        # Validate solution format
        if not isinstance(solution, dict):
            return False
        if "matrix" not in solution or "translation" not in solution:
            return False
        matrix = solution["matrix"]
        translation = solution["translation"]
        if (not isinstance(matrix, list) or len(matrix) != 2 or
                not all(isinstance(row, list) and len(row) == 2 for row in matrix)):
            return False
        if (not isinstance(translation, list) or len(translation) != 2):
            return False

        # Reconstruct transformation
        a, b_coef = matrix[0]
        c, d = matrix[1]
        tx, ty = translation

        # Validate against problem data
        if not isinstance(problem, dict):
            return False
        if "points" not in problem or "targets" not in problem:
            return False
        points = problem["points"]
        targets = problem["targets"]
        if len(points) != len(targets):
            return False

        tol = 1e-6
        for (x, y), (xp, yp) in zip(points, targets):
            x_pred = a * x + b_coef * y + tx
            y_pred = c * x + d * y + ty
            if abs(x_pred - xp) > tol or abs(y_pred - yp) > tol:
                return False
        return True
