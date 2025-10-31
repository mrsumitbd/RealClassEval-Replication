
class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # Identity matrix

    def solve(self, problem):
        # Assuming problem is a list of tuples (x, y) and we need to apply the transformation
        transformed_points = []
        for point in problem:
            x, y = point
            # Apply the affine transformation
            new_x = self.matrix[0][0] * x + \
                self.matrix[0][1] * y + self.matrix[0][2]
            new_y = self.matrix[1][0] * x + \
                self.matrix[1][1] * y + self.matrix[1][2]
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
        transformed_points = self.solve(problem)
        return transformed_points == solution
