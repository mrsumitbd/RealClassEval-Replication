
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

        # Compute the affine transformation matrix
        A = np.zeros((6, 6))
        b = np.zeros(6)

        for i in range(3):
            x, y = src_points[i]
            u, v = dst_points[i]

            A[2*i, :] = [x, y, 1, 0, 0, 0]
            A[2*i+1, :] = [0, 0, 0, x, y, 1]

            b[2*i] = u
            b[2*i+1] = v

        # Solve for the affine transformation parameters
        params = np.linalg.lstsq(A, b, rcond=None)[0]

        # Format the solution as expected by the task
        solution = {
            'matrix': params.reshape((2, 3)).tolist()
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
        matrix = np.array(solution['matrix'])

        # Check if the solution transforms the source points to the destination points
        transformed_points = np.dot(
            np.hstack((src_points, np.ones((src_points.shape[0], 1)))), matrix.T)

        # Check if the transformed points are close to the destination points
        return np.allclose(transformed_points, dst_points)
