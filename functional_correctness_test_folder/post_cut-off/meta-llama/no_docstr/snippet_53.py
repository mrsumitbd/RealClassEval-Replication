
import numpy as np


class AffineTransform2D:

    def __init__(self):
        self.matrix = np.eye(3)

    def solve(self, problem):
        """
        problem is expected to be a list of 3 pairs of corresponding points.
        Each point is a tuple of two numbers.
        """
        if len(problem) != 3:
            raise ValueError("Exactly 3 pairs of points are required")

        src_points = np.array([list(point[0]) + [1] for point in problem])
        dst_points = np.array([list(point[1]) + [1] for point in problem])

        try:
            self.matrix = np.linalg.solve(src_points.T, dst_points.T).T
        except np.linalg.LinAlgError:
            raise ValueError("The given points are linearly dependent")

    def is_solution(self, problem, solution):
        """
        problem is a list of pairs of corresponding points.
        solution is a list of points.
        """
        if len(problem) != len(solution):
            return False

        for (src, dst), sol in zip(problem, solution):
            src_homogeneous = np.array(list(src) + [1])
            dst_homogeneous = np.dot(self.matrix, src_homogeneous)
            dst_homogeneous /= dst_homogeneous[2]
            if not np.allclose(dst_homogeneous[:2], sol):
                return False

        return True
