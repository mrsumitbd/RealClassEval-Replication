
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
        Returns:
            The solution in the format expected by the task
        '''
        # Extract points from the problem
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])

        # Calculate the affine transformation matrix
        A = np.zeros((2 * len(src_points), 6))
        B = np.zeros((2 * len(src_points), 1))

        for i, (src, dst) in enumerate(zip(src_points, dst_points)):
            x, y = src
            u, v = dst
            A[2 * i] = [x, y, 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, x, y, 1]
            B[2 * i] = u
            B[2 * i + 1] = v

        # Solve for the affine transformation parameters
        params, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
        # Add the last parameter which is 1 for affine transformation
        params = np.append(params, 1)

        # Reshape parameters to form the transformation matrix
        transformation_matrix = params.reshape((2, 3))

        return transformation_matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Extract points from the problem
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])

        # Apply the transformation matrix to the source points
        src_points_homogeneous = np.hstack(
            (src_points, np.ones((src_points.shape[0], 1))))
        transformed_points = np.dot(src_points_homogeneous, solution.T)

        # Check if the transformed points match the destination points
        return np.allclose(transformed_points, dst_points)
