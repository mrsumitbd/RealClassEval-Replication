
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
        source_points = problem['source_points']
        target_points = problem['target_points']

        # At least 3 points are needed to solve for affine transformation
        if len(source_points) < 3 or len(target_points) < 3:
            return None

        # Construct the matrix A and vector b for the least squares problem A * x = b
        A = []
        b = []
        for (x_src, y_src), (x_tgt, y_tgt) in zip(source_points, target_points):
            A.append([x_src, y_src, 1, 0, 0, 0])
            A.append([0, 0, 0, x_src, y_src, 1])
            b.append(x_tgt)
            b.append(y_tgt)

        # Solve the least squares problem
        import numpy as np
        A_np = np.array(A)
        b_np = np.array(b)
        x, residuals, rank, singular_values = np.linalg.lstsq(
            A_np, b_np, rcond=None)

        # Extract the affine transformation parameters
        a, b, c, d, e, f = x
        transformation_matrix = [[a, b, c], [d, e, f]]

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
        if solution is None:
            return False

        source_points = problem['source_points']
        target_points = problem['target_points']

        if len(source_points) != len(target_points):
            return False

        a, b, c = solution[0]
        d, e, f = solution[1]

        for (x_src, y_src), (x_tgt, y_tgt) in zip(source_points, target_points):
            x_pred = a * x_src + b * y_src + c
            y_pred = d * x_src + e * y_src + f
            if not (abs(x_pred - x_tgt) < 1e-6 and abs(y_pred - y_tgt) < 1e-6):
                return False

        return True
