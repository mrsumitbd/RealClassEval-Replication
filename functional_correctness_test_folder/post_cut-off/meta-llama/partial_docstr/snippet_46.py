
import numpy as np


class AffineTransform2D:

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
        src = np.array(problem['src'])
        dst = np.array(problem['dst'])

        # Calculate the affine transformation matrix
        A = np.vstack([src.T, np.ones(src.shape[0])]).T
        M = np.linalg.lstsq(A, dst, rcond=None)[0].T

        # Extract the linear transformation matrix and translation vector
        linear_transformation = M[:, :2]
        translation = M[:, 2]

        # Format the solution
        solution = {
            'linear_transformation': linear_transformation.tolist(),
            'translation': translation.tolist()
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
        src = np.array(problem['src'])
        dst = np.array(problem['dst'])

        linear_transformation = np.array(solution['linear_transformation'])
        translation = np.array(solution['translation'])

        # Apply the affine transformation to the source points
        transformed_src = np.dot(src, linear_transformation.T) + translation

        # Check if the transformed source points match the destination points
        return np.allclose(transformed_src, dst)
