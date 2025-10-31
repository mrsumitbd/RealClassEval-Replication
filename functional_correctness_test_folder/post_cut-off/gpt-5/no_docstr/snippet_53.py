import numpy as np


class AffineTransform2D:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Expects problem to be one of:
        - dict with 'src' and 'dst' arrays/lists of shape (N,2), N>=3
        - dict with 'pairs': iterable of ((x, y), (X, Y))
        Optionally 'weights' (length N) and 'regularization' (float) and 'tol' (float)
        Returns a 2x3 numpy array representing the affine transform:
        [[a11, a12, tx],
         [a21, a22, ty]]
        """
        src, dst, weights, reg = self._parse_problem(problem)
        if src.shape[0] < 3:
            raise ValueError(
                "At least 3 point correspondences are required for 2D affine estimation.")
        A, b = self._build_system(src, dst, weights)
        if reg is not None and reg > 0:
            # Tikhonov regularization on linear terms (a11, a12, a21, a22), leave translation unregularized
            L = np.zeros((4, 6))
            L[0, 0] = 1.0
            L[1, 1] = 1.0
            L[2, 2] = 1.0
            L[3, 3] = 1.0
            A = np.vstack([A, np.sqrt(reg) * L])
            b = np.concatenate([b, np.zeros(4)])
        x, *_ = np.linalg.lstsq(A, b, rcond=None)
        M = np.array([[x[0], x[1], x[4]],
                      [x[2], x[3], x[5]]], dtype=float)
        return M

    def is_solution(self, problem, solution):
        """
        Checks whether the provided solution (2x3 matrix) maps problem['src'] to problem['dst']
        within tolerance problem.get('tol', 1e-6). Returns True/False.
        """
        src, dst, _, _ = self._parse_problem(problem)
        tol = float(problem.get('tol', 1e-6)
                    ) if isinstance(problem, dict) else 1e-6

        M = np.asarray(solution, dtype=float)
        if M.shape != (2, 3):
            return False

        pred = self._apply_affine(M, src)
        if dst.shape != pred.shape:
            return False

        err = np.linalg.norm(pred - dst, axis=1)
        # Use max error to be strict; allow both absolute and relative tolerance
        max_err = float(np.max(err)) if err.size else 0.0
        if max_err <= tol:
            return True
        # If scales are large, allow relative tolerance as fallback
        scale = max(1.0, float(np.max(np.linalg.norm(dst, axis=1)))
                    ) if dst.size else 1.0
        return max_err <= tol * scale

    def _parse_problem(self, problem):
        if isinstance(problem, dict):
            if 'pairs' in problem and problem['pairs'] is not None:
                pairs = list(problem['pairs'])
                if len(pairs) == 0:
                    src = np.zeros((0, 2), dtype=float)
                    dst = np.zeros((0, 2), dtype=float)
                else:
                    src = np.asarray([p[0] for p in pairs],
                                     dtype=float).reshape(-1, 2)
                    dst = np.asarray([p[1] for p in pairs],
                                     dtype=float).reshape(-1, 2)
            elif 'src' in problem and 'dst' in problem:
                src = np.asarray(problem['src'], dtype=float).reshape(-1, 2)
                dst = np.asarray(problem['dst'], dtype=float).reshape(-1, 2)
            else:
                raise ValueError(
                    "Problem must contain either 'pairs' or both 'src' and 'dst'.")
            if src.shape != dst.shape or src.shape[1] != 2:
                raise ValueError(
                    "Source and destination must have shape (N,2) and match.")
            weights = None
            if 'weights' in problem and problem['weights'] is not None:
                weights = np.asarray(
                    problem['weights'], dtype=float).reshape(-1)
                if weights.shape[0] != src.shape[0]:
                    raise ValueError(
                        "Weights length must match number of points.")
                if np.any(weights < 0):
                    raise ValueError("Weights must be non-negative.")
            reg = float(problem.get('regularization', 0.0)
                        ) if 'regularization' in problem else None
            return src, dst, weights, reg
        else:
            raise TypeError(
                "Problem must be a dict with keys defining correspondences.")

    def _build_system(self, src, dst, weights=None):
        n = src.shape[0]
        A = np.zeros((2 * n, 6), dtype=float)
        b = np.zeros((2 * n,), dtype=float)
        x = src[:, 0]
        y = src[:, 1]
        X = dst[:, 0]
        Y = dst[:, 1]
        # Row structure:
        # [x, y, 0, 0, 1, 0] * params = X
        # [0, 0, x, y, 0, 1] * params = Y
        A[0::2, 0] = x
        A[0::2, 1] = y
        A[0::2, 4] = 1.0
        b[0::2] = X

        A[1::2, 2] = x
        A[1::2, 3] = y
        A[1::2, 5] = 1.0
        b[1::2] = Y

        if weights is not None:
            w = np.sqrt(np.asarray(weights, dtype=float)).reshape(-1)
            if w.shape[0] != n:
                raise ValueError("Weights length must match number of points.")
            W = np.repeat(w, 2)
            A = A * W[:, None]
            b = b * W
        return A, b

    def _apply_affine(self, M, pts):
        pts = np.asarray(pts, dtype=float).reshape(-1, 2)
        # [x', y']^T = [a11 a12 tx; a21 a22 ty] * [x, y, 1]^T
        xy1 = np.hstack([pts, np.ones((pts.shape[0], 1), dtype=float)])
        return (M @ xy1.T).T
