
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
        Solve the affine transformation problem.
        Args:
            problem: A dictionary containing 'points' and 'transformed_points'.
                    Each is a list of 2D points (x, y).
        Returns:
            A 3x3 numpy array representing the affine transformation matrix.
        '''
        points = np.array(problem['points'])
        transformed_points = np.array(problem['transformed_points'])

        # Pad the points with ones for homogeneous coordinates
        A = np.column_stack([points, np.ones(len(points))])
        b = transformed_points

        # Solve for the transformation matrix using least squares
        transformation, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Construct the 3x3 affine transformation matrix
        affine_matrix = np.vstack([transformation.T, [0, 0, 1]])
        return affine_matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem (dict with 'points' and 'transformed_points').
            solution: The proposed solution (3x3 affine transformation matrix).
        Returns:
            True if the solution is valid, False otherwise.
        '''
        points = np.array(problem['points'])
        transformed_points = np.array(problem['transformed_points'])

        # Apply the transformation to the original points
        homogeneous_points = np.column_stack([points, np.ones(len(points))])
        predicted_points = (solution @ homogeneous_points.T).T[:, :2]

        # Check if the predicted points match the transformed points within a tolerance
        return np.allclose(predicted_points, transformed_points, atol=1e-6)
