class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def _to_float(self, v):
        try:
            return float(v)
        except Exception:
            return v

    def _is_int_like_number(self, x, eps=1e-9):
        if isinstance(x, bool):
            return False
        try:
            xf = float(x)
        except Exception:
            return False
        return abs(xf - round(xf)) <= eps

    def _all_int_like(self, iterable):
        for v in iterable:
            if isinstance(v, (list, tuple)):
                if not self._all_int_like(v):
                    return False
            else:
                if not self._is_int_like_number(v):
                    return False
        return True

    def _round_value(self, x, mode='auto', decimals=None):
        if decimals is not None:
            return round(x, int(decimals))
        if mode == 'nearest':
            return round(x)
        if mode == 'floor':
            import math
            return math.floor(x)
        if mode == 'ceil':
            import math
            return math.ceil(x)
        if mode == 'int':
            return int(round(x))
        # auto: keep as float unless very close to int
        if self._is_int_like_number(x):
            return int(round(x))
        return x

    def _parse_matrix_and_translation(self, problem):
        # Accept multiple key aliases
        A = problem.get('matrix')
        if A is None:
            A = problem.get('A')
        if A is None:
            A = problem.get('transform')
        t = problem.get('translation')
        if t is None:
            t = problem.get('t')

        # If a 3x3 homogeneous matrix is provided
        if A is not None and isinstance(A, (list, tuple)) and len(A) == 3 and all(
            isinstance(row, (list, tuple)) and len(row) == 3 for row in A
        ):
            H = [[self._to_float(A[i][j]) for j in range(3)] for i in range(3)]
            return H

        # If a 2x2 linear matrix is provided
        if A is not None and isinstance(A, (list, tuple)) and len(A) == 2 and all(
            isinstance(row, (list, tuple)) and len(row) == 2 for row in A
        ):
            a00 = self._to_float(A[0][0])
            a01 = self._to_float(A[0][1])
            a10 = self._to_float(A[1][0])
            a11 = self._to_float(A[1][1])
            tx, ty = 0.0, 0.0
            if t is not None and isinstance(t, (list, tuple)) and len(t) == 2:
                tx = self._to_float(t[0])
                ty = self._to_float(t[1])
            H = [
                [a00, a01, tx],
                [a10, a11, ty],
                [0.0, 0.0, 1.0],
            ]
            return H

        # If only translation provided
        if A is None and isinstance(t, (list, tuple)) and len(t) == 2:
            tx = self._to_float(t[0])
            ty = self._to_float(t[1])
            H = [
                [1.0, 0.0, tx],
                [0.0, 1.0, ty],
                [0.0, 0.0, 1.0],
            ]
            return H

        # If nothing valid provided, default to identity
        H = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        return H

    def _invert_3x3(self, H):
        # Invert a 3x3 matrix; assume last row [0,0,1] for affine, but handle generic
        # Compute adjugate/determinant
        a, b, c = H[0]
        d, e, f = H[1]
        g, h, i = H[2]
        det = (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g))
        if abs(det) < 1e-12:
            raise ValueError("Singular matrix cannot be inverted")
        inv_det = 1.0 / det
        adj = [
            [(e*i - f*h), -(b*i - c*h),  (b*f - c*e)],
            [-(d*i - f*g),  (a*i - c*g), -(a*f - c*d)],
            [(d*h - e*g), -(a*h - b*g),  (a*e - b*d)],
        ]
        inv = [[adj[r][c] * inv_det for c in range(3)] for r in range(3)]
        return inv

    def _matmul_3x3_vec3(self, H, v):
        return [
            H[0][0]*v[0] + H[0][1]*v[1] + H[0][2]*v[2],
            H[1][0]*v[0] + H[1][1]*v[1] + H[1][2]*v[2],
            H[2][0]*v[0] + H[2][1]*v[1] + H[2][2]*v[2],
        ]

    def _apply_transform(self, H, points):
        out = []
        for p in points:
            x = self._to_float(p[0])
            y = self._to_float(p[1])
            v = [x, y, 1.0]
            r = self._matmul_3x3_vec3(H, v)
            if abs(r[2]) > 1e-12:
                x2 = r[0] / r[2]
                y2 = r[1] / r[2]
            else:
                x2 = r[0]
                y2 = r[1]
            out.append([x2, y2])
        return out

    def _extract_points(self, problem):
        # Accept 'points' as list of [x,y], or 'point' as single [x,y]
        if 'points' in problem and isinstance(problem['points'], (list, tuple)):
            pts_raw = problem['points']
            pts = []
            for p in pts_raw:
                if isinstance(p, (list, tuple)) and len(p) == 2:
                    pts.append([self._to_float(p[0]), self._to_float(p[1])])
                else:
                    raise ValueError("Invalid point format")
            return pts, 'points'
        if 'point' in problem and isinstance(problem['point'], (list, tuple)) and len(problem['point']) == 2:
            p = problem['point']
            return [[self._to_float(p[0]), self._to_float(p[1])]], 'point'
        # Fallback: empty list
        return [], 'points'

    def _format_output(self, transformed, mode_key, rounding_mode, decimals):
        # Apply rounding
        formatted = []
        for x, y in transformed:
            x2 = self._round_value(x, rounding_mode, decimals)
            y2 = self._round_value(y, rounding_mode, decimals)
            formatted.append([x2, y2])
        if mode_key == 'point':
            return formatted[0] if formatted else [0, 0]
        return formatted

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary")

        points, mode_key = self._extract_points(problem)
        H = self._parse_matrix_and_translation(problem)

        # Optional pivot/origin support: translate to origin, apply H, translate back
        origin = problem.get('origin')
        pre = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        post = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        if isinstance(origin, (list, tuple)) and len(origin) == 2:
            ox = self._to_float(origin[0])
            oy = self._to_float(origin[1])
            pre = [
                [1.0, 0.0, -ox],
                [0.0, 1.0, -oy],
                [0.0, 0.0, 1.0],
            ]
            post = [
                [1.0, 0.0, ox],
                [0.0, 1.0, oy],
                [0.0, 0.0, 1.0],
            ]

        # Compose: H_total = post * H * pre
        def matmul_3x3(A, B):
            R = [[0.0]*3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    R[i][j] = A[i][0]*B[0][j] + \
                        A[i][1]*B[1][j] + A[i][2]*B[2][j]
            return R

        H_total = matmul_3x3(post, matmul_3x3(H, pre))

        # Inverse if requested
        inv_flag = bool(problem.get('inverse', False))
        if inv_flag:
            H_total = self._invert_3x3(H_total)

        transformed = self._apply_transform(H_total, points)

        # Determine rounding
        rounding_mode = 'auto'
        if 'round' in problem and isinstance(problem['round'], str):
            rm = problem['round'].strip().lower()
            if rm in ('nearest', 'round', 'int'):
                rounding_mode = 'nearest' if rm != 'int' else 'int'
            elif rm in ('floor', 'ceil'):
                rounding_mode = rm
        decimals = problem.get('decimals')
        if decimals is not None:
            try:
                decimals = int(decimals)
            except Exception:
                decimals = None

        # If no explicit rounding instructions, and inputs appear integer-like, round to nearest int
        if 'round' not in problem and decimals is None:
            # Check integrality of inputs: points, matrix, translation
            int_like = True
            pts_check = self._all_int_like(points)
            H_check = self._all_int_like(H)
            int_like = pts_check and H_check
            if int_like:
                rounding_mode = 'nearest'

        result = self._format_output(
            transformed, mode_key, rounding_mode, decimals)

        # Return in same structure that was provided if possible
        if mode_key == 'points':
            return result
        else:
            return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        def almost_equal(a, b, eps=1e-9):
            try:
                fa = float(a)
                fb = float(b)
                return abs(fa - fb) <= eps
            except Exception:
                return a == b

        # Accept either single point or list of points
        def normalize(sol, problem):
            if isinstance(sol, dict):
                if 'points' in sol:
                    return 'points', sol['points']
                if 'point' in sol:
                    return 'point', sol['point']
            # If problem had 'point', accept single [x,y]
            if 'point' in problem:
                return 'point', sol
            return 'points', sol

        key_e, exp = normalize(expected, problem)
        key_s, soln = normalize(solution, problem)

        # Compare
        if key_e == 'point':
            if not (isinstance(soln, (list, tuple)) and len(soln) == 2):
                return False
            return almost_equal(exp[0], soln[0]) and almost_equal(exp[1], soln[1])

        # points list
        if not isinstance(soln, (list, tuple)):
            return False
        if len(exp) != len(soln):
            return False
        for p_exp, p_sol in zip(exp, soln):
            if not (isinstance(p_sol, (list, tuple)) and len(p_sol) == 2):
                return False
            if not (almost_equal(p_exp[0], p_sol[0]) and almost_equal(p_exp[1], p_sol[1])):
                return False
        return True
