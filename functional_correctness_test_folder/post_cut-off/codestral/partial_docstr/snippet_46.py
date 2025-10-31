
class AffineTransform2D:

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.matrix = None

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        from numpy import array, linalg

        src = array(problem['src'])
        dst = array(problem['dst'])

        A = []
        for i in range(len(src)):
            A.append([src[i][0], src[i][1], 1, 0, 0, 0])
            A.append([0, 0, 0, src[i][0], src[i][1], 1])

        b = []
        for i in range(len(dst)):
            b.append(dst[i][0])
            b.append(dst[i][1])

        A = array(A)
        b = array(b)

        x = linalg.lstsq(A, b, rcond=None)[0]

        self.matrix = array(
            [[x[0], x[1], x[2]], [x[3], x[4], x[5]], [0, 0, 1]])

        return self.matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        from numpy import array, allclose

        src = array(problem['src'])
        dst = array(problem['dst'])

        transformed_src = []
        for point in src:
            x, y = point
            x_transformed = solution[0, 0] * x + \
                solution[0, 1] * y + solution[0, 2]
            y_transformed = solution[1, 0] * x + \
                solution[1, 1] * y + solution[1, 2]
            transformed_src.append([x_transformed, y_transformed])

        transformed_src = array(transformed_src)

        return allclose(transformed_src, dst, rtol=1e-5, atol=1e-5)
