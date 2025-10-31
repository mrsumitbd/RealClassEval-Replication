
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
        source_points = np.array(problem['source_points'])
        target_points = np.array(problem['target_points'])

        # Pad the data with ones for homogeneous coordinates
        n = source_points.shape[0]
        X = np.hstack([source_points, np.ones((n, 1))])
        Y = target_points

        # Solve for the transformation matrix using least squares
        A = np.linalg.lstsq(X, Y, rcond=None)[0]

        # Extract the affine transformation parameters
        solution = {
            'transform': A.T.tolist(),
            'residual': np.linalg.norm(Y - X @ A)
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
        try:
            source_points = np.array(problem['source_points'])
            target_points = np.array(problem['target_points'])
            transform = np.array(solution['transform'])

            # Apply the transformation to source points
            n = source_points.shape[0]
            X = np.hstack([source_points, np.ones((n, 1))])
            transformed_points = X @ transform.T

            # Check if transformed points are close to target points
            return np.allclose(transformed_points, target_points, atol=1e-6)
        except:
            return False
