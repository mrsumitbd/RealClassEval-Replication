
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
        source_points = np.array(problem['source'])
        target_points = np.array(problem['target'])

        # Calculate the affine transformation matrix
        A = np.vstack([source_points.T, np.ones((1, len(source_points)))]).T
        B = target_points

        # Solve for the affine transformation matrix using least squares
        affine_matrix = np.linalg.lstsq(A, B, rcond=None)[0].T

        # Predict the target points using the affine transformation matrix
        predicted_target_points = np.dot(affine_matrix, np.vstack([source_points.T, np.ones((1, len(source_points))]))).T

        return predicted_target_points.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        source_points = np.array(problem['source'])
        target_points = np.array(problem['target'])
        solution_points = np.array(solution)

        # Check if the number of points in the solution matches the number of target points
        if len(solution_points) != len(target_points):
            return False

        # Check if the solution points are close enough to the target points
        return np.allclose(solution_points, target_points)
