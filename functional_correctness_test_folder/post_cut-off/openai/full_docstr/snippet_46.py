
import math
from typing import Dict, List, Tuple, Any


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def solve(self, problem: Dict[str, Any]) -> List[List[float]]:
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
                     Expected keys:
                         - 'src': List[Tuple[float, float]] source points
                         - 'dst': List[Tuple[float, float]] destination points
        Returns:
            The solution as a 2x3 matrix [[a11, a12, a13], [a21, a22, a23]]
        '''
        src = problem.get('src')
        dst = problem.get('dst')
        if src is None or dst is None:
            raise ValueError("Problem must contain 'src' and 'dst' keys.")
        if len(src) != len(dst):
            raise ValueError(
                "Source and destination must have the same number of points.")
        n = len(src)
        if n < 3:
            raise ValueError(
                "At least 3 point correspondences are required to determine an affine transform.")

        # Build linear system: X * a = b
        # X shape: (2n, 6), a shape: (6,), b shape: (2n,)
        X = []
        b = []
        for (x, y), (xp, yp) in zip(src, dst):
            X.append([x, y, 1, 0, 0, 0])
            X.append([0, 0, 0, x, y, 1])
            b.append(xp)
            b.append(yp)

        # Solve least squares: a = (X^T X)^{-1} X^T b
        # Use simple Gaussian elimination for small systems
        # Convert to float
        X = [[float(v) for v in row] for row in X]
        b = [float(v) for v in b]

        # Augmented matrix
        aug = [row + [b_val] for row, b_val in zip(X, b)]
        m = len(aug)
        ncol = 6

        # Gaussian elimination
        for col in range(ncol):
            # Find pivot
            pivot_row = max(range(col, m), key=lambda r: abs(aug[r][col]))
            if abs(aug[pivot_row][col]) < 1e-12:
                continue  # skip singular
            # Swap
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
            # Normalize pivot row
            pivot = aug[col][col]
            aug[col] = [v / pivot for v in aug[col]]
            # Eliminate below
            for r in range(col + 1, m):
                factor = aug[r][col]
                aug[r] = [rv - factor * pv for rv, pv in zip(aug[r], aug[col])]

        # Back substitution
        a = [0.0] * ncol
        for i in range(ncol - 1, -1, -1):
            # Find first non-zero coefficient in row i
            row = aug[i]
            # Skip if row is all zeros
            if all(abs(v) < 1e-12 for v in row[:-1]):
                a[i] = 0.0
                continue
            # Find pivot column
            pivot_col = next(j for j in range(ncol) if abs(row[j]) > 1e-12)
            rhs = row[-1]
            for j in range(pivot_col + 1, ncol):
                rhs -= row[j] * a[j]
            a[pivot_col] = rhs / row[pivot_col]

        # Reshape to 2x3 matrix
        matrix = [[a[0], a[1], a[2]],
                  [a[3], a[4], a[5]]]
        return matrix

    def is_solution(self, problem: Dict[str, Any], solution: List[List[float]]) -> bool:
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        src = problem.get('src')
        dst = problem.get('dst')
        if src is None or dst is None or solution is None:
            return False
        if len(src) != len(dst):
            return False
        if len(solution) != 2 or len(solution[0]) != 3 or len(solution[1]) != 3:
            return False

        a11, a12, a13 = solution[0]
        a21, a22, a23 = solution[1]

        tol = 1e-6
        for (x, y), (xp, yp) in zip(src, dst):
            x_est = a11 * x + a12 * y + a13
            y_est = a21 * x + a22 * y + a23
            if abs(x_est - xp) > tol or abs(y_est - yp) > tol:
                return False
        return True
