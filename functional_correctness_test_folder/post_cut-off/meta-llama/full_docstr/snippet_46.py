
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
        A = np.zeros((6, 6))
        b = np.zeros(6)

        for i in range(3):
            x, y = src_points[i]
            u, v = dst_points[i]
            A[i*2, :] = [x, y, 1, 0, 0, 0]
            A[i*2 + 1, :] = [0, 0, 0, x, y, 1]
            b[i*2] = u
            b[i*2 + 1] = v

        # Solve for the affine transformation parameters
        params = np.linalg.solve(A, b)

        # Reshape the parameters into a 2x3 matrix
        transform_matrix = np.array([[params[0], params[1], params[2]],
                                     [params[3], params[4], params[5]]])

        return {'transform_matrix': transform_matrix.tolist()}

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
        transform_matrix = np.array(solution['transform_matrix'])

        # Apply the affine transformation to the source points
        transformed_points = np.dot(
            np.hstack((src_points, np.ones((src_points.shape[0], 1)))), transform_matrix.T)

        # Check if the transformed points match the destination points within a tolerance
        tolerance = 1e-6
        return np.allclose(transformed_points, dst_points, atol=tolerance)
