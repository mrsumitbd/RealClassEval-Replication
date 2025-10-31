class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.tol = 1e-9

    def _normalize_transform(self, T):
        # Accepts:
        # - 3x3 homogeneous matrix
        # - 2x3 affine matrix
        # - 2x2 linear matrix
        # Returns a normalized 3x3 homogeneous matrix
        if not isinstance(T, (list, tuple)):
            raise ValueError("Transform must be a list or tuple")
        rows = len(T)
        if rows == 0 or not hasattr(T[0], "__len__"):
            raise ValueError("Transform must be 2D")
        cols = len(T[0])

        # 3x3 homogeneous
        if rows == 3 and cols == 3:
            return [[float(T[i][j]) for j in range(3)] for i in range(3)]

        # 2x3 affine
        if rows == 2 and cols == 3:
            return [
                [float(T[0][0]), float(T[0][1]), float(T[0][2])],
                [float(T[1][0]), float(T[1][1]), float(T[1][2])],
                [0.0, 0.0, 1.0],
            ]

        # 2x2 linear
        if rows == 2 and cols == 2:
            return [
                [float(T[0][0]), float(T[0][1]), 0.0],
                [float(T[1][0]), float(T[1][1]), 0.0],
                [0.0, 0.0, 1.0],
            ]

        raise ValueError(
            "Unsupported transform shape. Expected 3x3, 2x3, or 2x2.")

    def _apply_to_point(self, T3, p):
        if not isinstance(p, (list, tuple)) or len(p) != 2:
            raise ValueError("Each point must be a 2-element list/tuple")
        x, y = float(p[0]), float(p[1])
        hx = T3[0][0] * x + T3[0][1] * y + T3[0][2] * 1.0
        hy = T3[1][0] * x + T3[1][1] * y + T3[1][2] * 1.0
        hw = T3[2][0] * x + T3[2][1] * y + T3[2][2] * 1.0
        if abs(hw) < self.tol:
            # Degenerate case; avoid division by zero. Treat as hw = 1.
            hw = 1.0
        return (hx / hw, hy / hw)

    def _get_points_from_problem(self, problem):
        if isinstance(problem, dict):
            if "points" in problem:
                pts = problem["points"]
                # Ensure it's a sequence of points
                if isinstance(pts, (list, tuple)) and (len(pts) == 0 or isinstance(pts[0], (list, tuple))):
                    return "list", list(pts)
            if "point" in problem:
                pt = problem["point"]
                if isinstance(pt, (list, tuple)) and len(pt) == 2:
                    return "single", [pt]
        # Fallback: if problem itself is a point or list of points
        if isinstance(problem, (list, tuple)):
            # single point
            if len(problem) == 2 and all(isinstance(v, (int, float)) for v in problem):
                return "single", [problem]
            # list of points
            if len(problem) > 0 and isinstance(problem[0], (list, tuple)) and len(problem[0]) == 2:
                return "list", list(problem)
        raise ValueError("Problem does not contain valid 'point' or 'points'")

    def _get_transform_from_problem(self, problem):
        candidates = []
        if isinstance(problem, dict):
            for k in ("transform", "matrix", "affine", "T"):
                if k in problem:
                    candidates.append(problem[k])
        if not candidates:
            raise ValueError(
                "Problem does not contain a transform under keys: 'transform', 'matrix', 'affine', or 'T'")
        return candidates[0]

    def solve(self, problem):
        mode, pts = self._get_points_from_problem(problem)
        T = self._get_transform_from_problem(problem)
        T3 = self._normalize_transform(T)

        # Optional rounding control
        digits = None
        if isinstance(problem, dict) and "round" in problem:
            try:
                digits = int(problem["round"])
            except Exception:
                digits = None

        out = []
        for p in pts:
            tp = self._apply_to_point(T3, p)
            if digits is not None:
                tp = (round(tp[0], digits), round(tp[1], digits))
            out.append(tp)

        if mode == "single":
            return out[0]
        return out

    def _almost_equal_point(self, a, b):
        if not (isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == 2 and len(b) == 2):
            return False
        return abs(float(a[0]) - float(b[0])) <= 1e-6 and abs(float(a[1]) - float(b[1])) <= 1e-6

    def is_solution(self, problem, solution):
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Compare shapes and values with tolerance
        # Single point
        if isinstance(expected, (list, tuple)) and len(expected) == 2 and not (
            len(expected) > 0 and isinstance(
                expected[0], (list, tuple)) and len(expected[0]) == 2
        ):
            # expected is a single point
            return self._almost_equal_point(expected, solution)

        # List of points
        if not isinstance(solution, (list, tuple)):
            return False
        if len(solution) != len(expected):
            return False
        for a, b in zip(expected, solution):
            if not self._almost_equal_point(a, b):
                return False
        return True
