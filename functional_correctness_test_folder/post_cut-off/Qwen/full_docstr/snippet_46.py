
class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # Identity matrix

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        if 'points' not in problem or 'transform' not in problem:
            raise ValueError(
                "Problem must contain 'points' and 'transform' keys.")

        points = problem['points']
        transform = problem['transform']

        if len(transform) != 6:
            raise ValueError("Transform must contain 6 parameters.")

        a, b, c, d, e, f = transform
        self.matrix = [[a, b, c], [d, e, f], [0, 0, 1]]

        transformed_points = []
        for point in points:
            x, y = point
            new_x = a * x + b * y + c
            new_y = d * x + e * y + f
            transformed_points.append((new_x, new_y))

        return transformed_points

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if 'points' not in problem:
            raise ValueError("Problem must contain 'points' key.")

        original_points = problem['points']

        if len(original_points) != len(solution):
            return False

        for original, transformed in zip(original_points, solution):
            if not self._is_point_transformed_correctly(original, transformed, problem['transform']):
                return False

        return True

    def _is_point_transformed_correctly(self, original, transformed, transform):
        a, b, c, d, e, f = transform
        x, y = original
        expected_x = a * x + b * y + c
        expected_y = d * x + e * y + f
        return (abs(expected_x - transformed[0]) < 1e-9) and (abs(expected_y - transformed[1]) < 1e-9)
