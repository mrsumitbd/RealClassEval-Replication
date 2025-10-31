class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    # -------------------- Public API --------------------

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        points = self._extract_points(problem)
        A, t = self._build_affine(problem)

        # Inverse transform if requested
        if self._get_bool(problem, ("inverse", "invert")):
            A, t = self._invert_affine(A, t)

        # Apply transform
        transformed = [self._apply_affine_point(p, A, t) for p in points]

        # Wrapping / clipping / rounding options
        transformed = self._postprocess_points(problem, transformed)

        return {
            "points": transformed,
            "matrix": [[A[0][0], A[0][1]], [A[1][0], A[1][1]]],
            "translation": [t[0], t[1]],
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Compute expected output from the problem
        expected_solution = self.solve(problem)
        expected_points = expected_solution.get("points")

        # Extract candidate points from solution
        candidate_points = self._extract_points_from_solution(solution)

        # If the problem has explicit expected output, prefer that for comparison
        explicit_expected = self._extract_expected(problem)
        if explicit_expected is not None:
            expected_points = explicit_expected

        if expected_points is None or candidate_points is None:
            return False

        return self._points_equal(expected_points, candidate_points, self._get_tolerance(problem))

    # -------------------- Helpers --------------------

    def _extract_points(self, problem):
        # Accept a variety of common keys for input points
        for key in ("points", "coords", "xy", "input", "vertices"):
            if key in problem:
                pts = problem[key]
                return self._normalize_points(pts)
        # If transform maps from "source" to "target", allow "source"
        if "source" in problem:
            return self._normalize_points(problem["source"])
        return []

    def _extract_expected(self, problem):
        # Accept multiple keys for expected/target output
        for key in ("expected", "target", "output", "solution", "transformed_points"):
            if key in problem:
                return self._normalize_points(problem[key])
        # If mapping source->target
        if "target" in problem:
            return self._normalize_points(problem["target"])
        return None

    def _extract_points_from_solution(self, solution):
        # Accept solution as list of points or dict containing points
        if solution is None:
            return None
        if isinstance(solution, dict):
            for key in ("points", "coords", "xy", "output", "transformed_points"):
                if key in solution:
                    return self._normalize_points(solution[key])
            # Fallback: try to interpret dict as point list if it looks like it
            if self._looks_like_points(solution):
                return self._normalize_points(solution)
            return None
        # If provided directly as list of points
        if isinstance(solution, (list, tuple)):
            return self._normalize_points(solution)
        return None

    def _looks_like_points(self, obj):
        if isinstance(obj, (list, tuple)):
            if not obj:
                return True
            return all(isinstance(p, (list, tuple)) and len(p) == 2 for p in obj)
        return False

    def _normalize_points(self, pts):
        # Convert a variety of input formats into list[[x, y], ...]
        if pts is None:
            return []
        if isinstance(pts, dict):
            # Possibly a dict with indices or named points: sort by key if keys are ints
            try:
                items = sorted(pts.items(), key=lambda kv: int(kv[0]))
            except Exception:
                items = list(pts.items())
            pts = [v for _, v in items]

        result = []
        for p in pts:
            if isinstance(p, (list, tuple)) and len(p) == 2:
                x, y = p
                result.append([self._to_float(x), self._to_float(y)])
            elif isinstance(p, dict) and "x" in p and "y" in p:
                result.append([self._to_float(p["x"]), self._to_float(p["y"])])
            else:
                # Skip invalid entries
                continue
        return result

    def _to_float(self, v):
        try:
            return float(v)
        except Exception:
            return 0.0

    def _get_bool(self, d, keys):
        for k in keys:
            if k in d:
                return bool(d[k])
        return False

    def _get_tolerance(self, problem):
        tol = problem.get("tolerance", None)
        if tol is None:
            tol = problem.get("tol", None)
        try:
            return float(tol) if tol is not None else 1e-9
        except Exception:
            return 1e-9

    # Affine building

    def _build_affine(self, problem):
        # Start with identity
        A = [[1.0, 0.0], [0.0, 1.0]]
        t = [0.0, 0.0]

        # If a matrix is directly provided, use it
        direct_matrix = self._get_matrix(problem)
        direct_translation = self._get_translation(problem)

        if direct_matrix is not None or direct_translation is not None:
            if direct_matrix is not None:
                A = direct_matrix
            if direct_translation is not None:
                t = direct_translation
            return A, t

        # Otherwise compose from components
        order = self._get_order(problem)
        center = self._get_center(problem)

        for op in order:
            op = op.lower()
            if op in ("scale", "scaling"):
                sx, sy = self._get_scale(problem)
                M = [[sx, 0.0], [0.0, sy]]
                u = self._centered_translation_for_matrix(M, center)
                A, t = self._compose(M, u, A, t)
            elif op in ("rotate", "rotation"):
                angle, radians = self._get_rotation(problem)
                c, s = self._cos_sin(angle, radians)
                M = [[c, -s], [s, c]]
                u = self._centered_translation_for_matrix(M, center)
                A, t = self._compose(M, u, A, t)
            elif op in ("shear", "skew"):
                shx, shy = self._get_shear(problem)
                # Compose x-shear then y-shear for clarity
                Mx = [[1.0, shx], [0.0, 1.0]]
                ux = self._centered_translation_for_matrix(Mx, center)
                A, t = self._compose(Mx, ux, A, t)
                My = [[1.0, 0.0], [shy, 1.0]]
                uy = self._centered_translation_for_matrix(My, center)
                A, t = self._compose(My, uy, A, t)
            elif op in ("shear_x", "skew_x"):
                shx, _ = self._get_shear(problem)
                M = [[1.0, shx], [0.0, 1.0]]
                u = self._centered_translation_for_matrix(M, center)
                A, t = self._compose(M, u, A, t)
            elif op in ("shear_y", "skew_y"):
                _, shy = self._get_shear(problem)
                M = [[1.0, 0.0], [shy, 1.0]]
                u = self._centered_translation_for_matrix(M, center)
                A, t = self._compose(M, u, A, t)
            elif op in ("translate", "translation", "offset", "shift", "move"):
                tr = self._get_translation(problem) or [0.0, 0.0]
                A, t = self._compose([[1.0, 0.0], [0.0, 1.0]], tr, A, t)
            # Unknown ops are ignored

        return A, t

    def _get_matrix(self, problem):
        # Read a 2x2 matrix from various fields
        candidates = [
            "matrix",
            "A",
            "affine_matrix",
            "linear",
            "linear_matrix",
            "rotation_matrix",
        ]
        for key in candidates:
            m = problem.get(key)
            M = self._as_2x2(m)
            if M is not None:
                return M
        return None

    def _as_2x2(self, m):
        if not m:
            return None
        try:
            if isinstance(m, dict):
                a = float(m.get("a", 1.0))
                b = float(m.get("b", 0.0))
                c = float(m.get("c", 0.0))
                d = float(m.get("d", 1.0))
                return [[a, b], [c, d]]
            if isinstance(m, (list, tuple)) and len(m) == 2:
                row0, row1 = m
                if isinstance(row0, (list, tuple)) and isinstance(row1, (list, tuple)) and len(row0) == 2 and len(row1) == 2:
                    return [[float(row0[0]), float(row0[1])], [float(row1[0]), float(row1[1])]]
        except Exception:
            return None
        return None

    def _get_translation(self, problem):
        for key in ("translation", "translate", "offset", "t", "bias", "shift", "move"):
            v = problem.get(key)
            if v is None:
                continue
            try:
                if isinstance(v, dict) and "x" in v and "y" in v:
                    return [float(v["x"]), float(v["y"])]
                if isinstance(v, (list, tuple)) and len(v) == 2:
                    return [float(v[0]), float(v[1])]
                if isinstance(v, (int, float)):
                    return [float(v), float(v)]
            except Exception:
                continue
        return None

    def _get_scale(self, problem):
        v = problem.get("scale", problem.get("scaling", None))
        sx, sy = 1.0, 1.0
        if v is None:
            # Try components
            sx = self._to_float(problem.get("scale_x", 1.0))
            sy = self._to_float(problem.get("scale_y", 1.0))
        else:
            if isinstance(v, (list, tuple)) and len(v) == 2:
                sx, sy = self._to_float(v[0]), self._to_float(v[1])
            elif isinstance(v, dict):
                sx = self._to_float(v.get("x", 1.0))
                sy = self._to_float(v.get("y", 1.0))
            else:
                sx = sy = self._to_float(v)
        return sx, sy

    def _get_rotation(self, problem):
        # Returns (angle, radians_flag)
        if "rotate" in problem:
            ang = problem.get("rotate")
            radians = bool(problem.get("radians", False))
            return self._to_float(ang), radians
        if "rotation" in problem:
            rot = problem.get("rotation")
            radians = bool(problem.get("radians", False))
            return self._to_float(rot), radians
        if "angle" in problem:
            radians = bool(problem.get("radians", False))
            return self._to_float(problem.get("angle")), radians
        return 0.0, False

    def _get_shear(self, problem):
        v = problem.get("shear", problem.get("skew", None))
        shx, shy = 0.0, 0.0
        if v is None:
            shx = self._to_float(problem.get(
                "shear_x", problem.get("skew_x", 0.0)))
            shy = self._to_float(problem.get(
                "shear_y", problem.get("skew_y", 0.0)))
        else:
            if isinstance(v, (list, tuple)) and len(v) == 2:
                shx, shy = self._to_float(v[0]), self._to_float(v[1])
            elif isinstance(v, dict):
                shx = self._to_float(v.get("x", 0.0))
                shy = self._to_float(v.get("y", 0.0))
            else:
                shx = self._to_float(v)
                shy = 0.0
        return shx, shy

    def _get_order(self, problem):
        order = problem.get("order", None)
        if isinstance(order, (list, tuple)) and order:
            return list(order)
        # Default order: scale -> rotate -> shear -> translate
        return ["scale", "rotate", "shear", "translate"]

    def _get_center(self, problem):
        center = problem.get("center", problem.get(
            "pivot", problem.get("origin", None)))
        if center is None:
            return None
        if isinstance(center, dict) and "x" in center and "y" in center:
            return [self._to_float(center["x"]), self._to_float(center["y"])]
        if isinstance(center, (list, tuple)) and len(center) == 2:
            return [self._to_float(center[0]), self._to_float(center[1])]
        return None

    def _centered_translation_for_matrix(self, M, center):
        if center is None:
            return [0.0, 0.0]
        # u = (I - M) @ center
        I_minus_M = [[1.0 - M[0][0], -M[0][1]], [-M[1][0], 1.0 - M[1][1]]]
        return self._mat_vec(I_minus_M, center)

    # Linear algebra basics

    def _compose(self, M, u, A, t):
        # Compose current cumulative transform (A, t) with new op (M, u):
        # new = M * (A * p + t) + u => A' = M*A, t' = M*t + u
        C = self._mat_mul(M, A)
        d = self._vec_add(self._mat_vec(M, t), u)
        return C, d

    def _apply_affine_point(self, p, A, t):
        return self._vec_add(self._mat_vec(A, p), t)

    def _invert_affine(self, A, t):
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        if abs(det) < 1e-18:
            # Non-invertible; return identity fallback
            return [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0]
        inv_det = 1.0 / det
        Ainv = [
            [A[1][1] * inv_det, -A[0][1] * inv_det],
            [-A[1][0] * inv_det,  A[0][0] * inv_det],
        ]
        tinv = self._scale_vec(self._mat_vec(Ainv, t), -1.0)
        return Ainv, tinv

    def _mat_mul(self, X, Y):
        return [
            [X[0][0] * Y[0][0] + X[0][1] * Y[1][0],
                X[0][0] * Y[0][1] + X[0][1] * Y[1][1]],
            [X[1][0] * Y[0][0] + X[1][1] * Y[1][0],
                X[1][0] * Y[0][1] + X[1][1] * Y[1][1]],
        ]

    def _mat_vec(self, M, v):
        return [
            M[0][0] * v[0] + M[0][1] * v[1],
            M[1][0] * v[0] + M[1][1] * v[1],
        ]

    def _vec_add(self, a, b):
        return [a[0] + b[0], a[1] + b[1]]

    def _scale_vec(self, a, s):
        return [a[0] * s, a[1] * s]

    def _cos_sin(self, angle, radians_flag):
        import math
        ang = angle if radians_flag else (angle * math.pi / 180.0)
        return math.cos(ang), math.sin(ang)

    # Post-processing: rounding, clipping, wrapping

    def _postprocess_points(self, problem, points):
        points = [p[:] for p in points]

        # Optional wrapping (modulo) by width/height or x/y
        wrap = problem.get("wrap", problem.get("mod", None))
        if wrap is not None:
            wx, wy = self._parse_wrap(wrap)
            if wx is not None and wy is not None and (wx != 0 or wy != 0):
                for p in points:
                    if wx:
                        p[0] = p[0] % wx
                    if wy:
                        p[1] = p[1] % wy

        # Optional clipping to bounds [xmin, ymin, xmax, ymax]
        clip = problem.get("clip", problem.get("bounds", None))
        if clip is not None:
            xmin, ymin, xmax, ymax = self._parse_bounds(clip)
            for p in points:
                p[0] = max(xmin, min(xmax, p[0]))
                p[1] = max(ymin, min(ymax, p[1]))

        # Rounding / integer casting
        points = self._round_points(problem, points)
        return points

    def _parse_wrap(self, wrap):
        # Returns (wx, wy) or (None, None)
        if isinstance(wrap, dict):
            wx = wrap.get("w", wrap.get("width", wrap.get("x", None)))
            wy = wrap.get("h", wrap.get("height", wrap.get("y", None)))
            return (int(wx) if wx is not None else None, int(wy) if wy is not None else None)
        if isinstance(wrap, (list, tuple)) and len(wrap) == 2:
            return (int(wrap[0]), int(wrap[1]))
        if isinstance(wrap, (int, float)):
            v = int(wrap)
            return v, v
        return None, None

    def _parse_bounds(self, b):
        # Returns xmin, ymin, xmax, ymax
        try:
            if isinstance(b, dict):
                xmin = float(
                    b.get("xmin", b.get("left", b.get("x0", float("-inf")))))
                ymin = float(
                    b.get("ymin", b.get("bottom", b.get("y0", float("-inf")))))
                xmax = float(
                    b.get("xmax", b.get("right", b.get("x1", float("inf")))))
                ymax = float(
                    b.get("ymax", b.get("top", b.get("y1", float("inf")))))
                return xmin, ymin, xmax, ymax
            if isinstance(b, (list, tuple)) and len(b) == 4:
                return float(b[0]), float(b[1]), float(b[2]), float(b[3])
        except Exception:
            pass
        return float("-inf"), float("-inf"), float("inf"), float("inf")

    def _round_points(self, problem, points):
        # Determine rounding mode
        as_int = bool(problem.get("int", problem.get("integer", False)))
        round_flag = problem.get("round", None)
        ceil_flag = bool(problem.get("ceil", False))
        floor_flag = bool(problem.get("floor", False))
        digits = None

        if isinstance(round_flag, bool):
            digits = 0 if round_flag else None
        elif isinstance(round_flag, (int, float)):
            # If non-integer, treat as digits after decimal; if integer, digits count
            try:
                digits = int(round_flag)
            except Exception:
                digits = None

        import math
        out = []
        for x, y in points:
            if ceil_flag:
                x2, y2 = math.ceil(x), math.ceil(y)
            elif floor_flag:
                x2, y2 = math.floor(x), math.floor(y)
            elif digits is not None:
                x2, y2 = round(x, digits), round(y, digits)
            else:
                x2, y2 = x, y

            if as_int:
                x2, y2 = int(round(x2)), int(round(y2))
            out.append([x2, y2])
        return out

    # Comparison

    def _points_equal(self, a, b, tol):
        if len(a) != len(b):
            return False
        for p, q in zip(a, b):
            if not self._point_equal(p, q, tol):
                return False
        return True

    def _point_equal(self, p, q, tol):
        try:
            return abs(p[0] - q[0]) <= tol and abs(p[1] - q[1]) <= tol
        except Exception:
            return False
