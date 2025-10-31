
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

        # Create the matrix A for the linear system
        A = np.zeros((2 * len(src_points), 6))
        for i, (x, y) in enumerate(src_points):
            A[2 * i] = [x, y, 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, x, y, 1]

        # Create the vector b for the linear system
        b = dst_points.flatten()

        # Solve the linear system using least squares
        x, _, _, _ = lstsq(A, b)

        # Reshape the solution into a 2x3 matrix
        transform_matrix = x.reshape(2, 3)

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

        # Apply the transformation to the source points
        transformed_points = np.hstack(
            (src_points, np.ones((len(src_points), 1)))) @ transform_matrix.T

        # Check if the transformed points are close to the destination points
        return np.allclose(transformed_points, dst_points)
