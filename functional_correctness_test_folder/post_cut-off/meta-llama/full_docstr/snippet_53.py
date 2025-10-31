
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
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])

        # Calculate the affine transformation matrix
        A = np.vstack([src_points.T, np.ones(src_points.shape[0])]).T
        M = np.linalg.lstsq(A, dst_points, rcond=None)[0].T

        # Format the solution as expected
        solution = {
            'matrix': M.tolist()
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
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])
        M = np.array(solution['matrix'])

        # Apply the affine transformation to the source points
        transformed_points = np.dot(
            np.vstack([src_points.T, np.ones(src_points.shape[0])]).T, M.T)

        # Check if the transformed points match the destination points within a tolerance
        tolerance = 1e-6
        return np.allclose(transformed_points, dst_points, atol=tolerance)
