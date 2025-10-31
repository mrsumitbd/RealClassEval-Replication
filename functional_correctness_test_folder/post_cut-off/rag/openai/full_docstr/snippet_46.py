
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

    def _extract_points(self, problem):
        """
        Helper to extract source and target points from the problem dictionary.
        Supports multiple key names for flexibility.
        """
        # Source points
        if 'src' in problem:
            src = problem['src']
        elif 'points' in problem:
            src = problem['points']
        else:
            raise KeyError(
                "Problem dictionary must contain 'src' or 'points' key.")

        # Target points
        if 'dst' in problem:
            dst = problem['dst']
        elif 'target_points' in problem:
            dst = problem['target_points']
        else:
            raise KeyError(
                "Problem dictionary must contain 'dst' or 'target_points' key.")

        # Convert to numpy arrays
        src = np.asarray(src, dtype=float)
        dst = np.asarray(dst, dtype=float)

        if src.ndim != 2 or src.shape[1] != 2:
            raise ValueError("Source points must be an Nx2 array.")
        if dst.ndim != 2 or dst.shape[1] != 2:
            raise ValueError("Target points must be an Nx2 array.")
        if src.shape[0] != dst.shape[0]:
            raise ValueError(
                "Source and target must have the same number of points.")

        return src, dst

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        src, dst = self._extract_points(problem)

        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 point correspondences are required to determine a unique affine transform.")

        # Build the linear system A * params = b
        # params = [a, b, c, d, e, f]
        A = np.zeros((2 * n, 6), dtype=float)
        b = np.zeros(2 * n, dtype=float)

        for i in range(n):
            x, y = src[i]
            x_prime, y_prime = dst[i]
            # Equation for x'
            A[2 * i] = [x, y, 1, 0, 0, 0]
            b[2 * i] = x_prime
            # Equation for y'
            A[2 * i + 1] = [0, 0, 0, x, y, 1]
            b[2 * i + 1] = y_prime

        # Solve using least squares (handles overdetermined systems)
        params, *_ = np.linalg.lstsq(A, b, rcond=None)
        a, b_coef, c, d, e, f = params

        # Return as a 2x3 matrix
        matrix = [[a, b_coef, c], [d, e, f]]
        return matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        src, dst = self._extract_points(problem)

        # Ensure solution is a 2x3 matrix
        if not (isinstance(solution, (list, tuple)) and len(solution) == 2):
            return False
        if not (isinstance(solution[0], (list, tuple)) and len(solution[0]) == 3):
            return False
        if not (isinstance(solution[1], (list, tuple)) and len(solution[1]) == 3):
            return False

        a, b_coef, c = solution[0]
        d, e, f = solution[1]

        # Apply transformation to all source points
        transformed = np.empty_like(src)
        transformed[:, 0] = a * src[:, 0] + b_coef * src[:, 1] + c
        transformed[:, 1] = d * src[:, 0] + e * src[:, 1] + f

        # Compare with target points within a tolerance
        return np.allclose(transformed, dst, atol=1e-6, rtol=1e-6)
