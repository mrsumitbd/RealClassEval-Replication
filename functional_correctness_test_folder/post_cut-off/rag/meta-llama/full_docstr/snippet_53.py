
import numpy as np
from scipy.linalg import lstsq


class AffineTransform2D:
    """Initial implementation of affine_transform_2d task.

    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the AffineTransform2D."""
        pass

    def solve(self, problem):
        """Solve the affine_transform_2d problem.

        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d

        Returns:
            The solution in the format expected by the task
        """
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])

        A = np.vstack([src_points.T, np.ones((1, src_points.shape[0]))]).T
        B = dst_points.T

        x, _, _, _ = lstsq(A, B[0])
        y, _, _, _ = lstsq(A, B[1])

        transform_matrix = np.array(
            [[x[0], x[1], x[2]], [y[0], y[1], y[2]], [0, 0, 1]])

        return {'transform_matrix': transform_matrix.tolist()}

    def is_solution(self, problem, solution):
        """Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])
        transform_matrix = np.array(solution['transform_matrix'])

        transformed_points = np.dot(transform_matrix, np.vstack(
            (src_points.T, np.ones((1, src_points.shape[0])))))
        transformed_points = transformed_points[:2].T

        return np.allclose(transformed_points, dst_points)
