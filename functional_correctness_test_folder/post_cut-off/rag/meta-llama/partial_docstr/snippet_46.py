
import numpy as np
from scipy.linalg import lstsq


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
        Returns:
            The solution in the format expected by the task
        '''
        src_points = np.array(problem['src'])
        dst_points = np.array(problem['dst'])

        # Create the matrix A for the linear system
        A = np.zeros((2 * len(src_points), 6))
        for i, (x, y) in enumerate(src_points):
            A[2 * i] = [x, y, 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, x, y, 1]

        # Create the vector b for the linear system
        b = dst_points.flatten()

        # Solve the linear system using least squares
        x, _, _, _ = lstsq(A, b)

        # Reshape the solution into the affine transformation matrix
        affine_matrix = np.array(
            [[x[0], x[1], x[2]], [x[3], x[4], x[5]], [0, 0, 1]])

        return affine_matrix.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        src_points = np.array(problem['src'])
        dst_points = np.array(problem['dst'])

        # Convert the solution to a numpy array
        affine_matrix = np.array(solution)

        # Check if the affine matrix is valid (i.e., it has the correct shape)
        if affine_matrix.shape != (3, 3):
            return False

        # Check if the affine transformation maps the source points to the destination points
        transformed_points = np.dot(
            np.hstack((src_points, np.ones((len(src_points), 1)))), affine_matrix.T)[:, :2]
        return np.allclose(transformed_points, dst_points)
