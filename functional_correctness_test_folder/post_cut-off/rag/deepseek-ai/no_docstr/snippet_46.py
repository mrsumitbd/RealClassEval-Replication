
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
        source_points = problem['source_points']
        target_points = problem['target_points']

        # Construct the matrix A and vector b for the least squares problem
        A = []
        b = []
        for (x_src, y_src), (x_tgt, y_tgt) in zip(source_points, target_points):
            A.append([x_src, y_src, 1, 0, 0, 0])
            A.append([0, 0, 0, x_src, y_src, 1])
            b.append(x_tgt)
            b.append(y_tgt)

        # Solve the least squares problem
        import numpy as np
        A = np.array(A)
        b = np.array(b)
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Construct the affine transformation matrix
        solution = {
            'transform': [
                [params[0], params[1], params[2]],
                [params[3], params[4], params[5]],
                [0, 0, 1]
            ]
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
        import numpy as np

        transform = np.array(solution['transform'])
        source_points = problem['source_points']
        target_points = problem['target_points']

        for (x_src, y_src), (x_tgt, y_tgt) in zip(source_points, target_points):
            # Apply the transformation
            src_vec = np.array([x_src, y_src, 1])
            transformed = np.dot(transform, src_vec)

            # Check if the transformed point matches the target (within a small tolerance)
            if not np.allclose(transformed[:2], [x_tgt, y_tgt], atol=1e-6):
                return False
        return True
