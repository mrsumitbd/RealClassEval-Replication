
import numpy as np


class AffineTransform2D:

    def __init__(self):
        pass

    def solve(self, problem):
        # problem: {'source': [(x1, y1), ...], 'target': [(x1', y1'), ...]}
        src = np.array(problem['source'])
        tgt = np.array(problem['target'])
        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine an affine transformation in 2D.")
        # Build matrix A and vector b for least squares
        A = []
        b = []
        for i in range(n):
            x, y = src[i]
            x_p, y_p = tgt[i]
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(x_p)
            b.append(y_p)
        A = np.array(A)
        b = np.array(b)
        # Solve for affine parameters
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        # params: [a, b, c, d, e, f]
        return params.tolist()

    def is_solution(self, problem, solution):
        # solution: [a, b, c, d, e, f]
        a, b, c, d, e, f = solution
        src = problem['source']
        tgt = problem['target']
        for (x, y), (x_p, y_p) in zip(src, tgt):
            x_calc = a * x + b * y + c
            y_calc = d * x + e * y + f
            if not (np.isclose(x_calc, x_p, atol=1e-6) and np.isclose(y_calc, y_p, atol=1e-6)):
                return False
        return True
