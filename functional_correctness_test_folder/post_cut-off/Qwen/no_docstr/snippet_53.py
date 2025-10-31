
class AffineTransform2D:

    def __init__(self, matrix=None, vector=None):
        if matrix is None:
            matrix = [[1, 0], [0, 1]]
        if vector is None:
            vector = [0, 0]
        self.matrix = matrix
        self.vector = vector

    def solve(self, problem):
        # Assuming problem is a tuple (x, y) and we solve for the transformed point
        x, y = problem
        new_x = self.matrix[0][0] * x + self.matrix[0][1] * y + self.vector[0]
        new_y = self.matrix[1][0] * x + self.matrix[1][1] * y + self.vector[1]
        return (new_x, new_y)

    def is_solution(self, problem, solution):
        # Check if applying the affine transformation to problem results in solution
        transformed = self.solve(problem)
        return transformed == solution
