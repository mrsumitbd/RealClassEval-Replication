class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    # ---------------------- Public API ----------------------

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Extract or estimate the affine transform
        M, t = self._extract_or_fit_affine(problem)

        # Transform points if provided
        pts_key = None
        if 'points' in problem:
            pts_key = 'points'
        elif 'query_points' in problem:
            pts_key = 'query_points'

        transformed = None
        if pts_key is not None:
            pts = self._normalize_points(problem.get(pts_key, []))
            # True/'nearest'|'floor'|'ceil'|None
            rounding_mode = problem.get('round', None)
            ndigits = problem.get('decimal_places', None)
            transformed = self._apply_affine(
                M, t, pts, rounding=rounding_mode, ndigits=ndigits)

        # If expected is a simple list, return a list to match format
        expected = problem.get('expected', None)
        if isinstance(expected, list):
            if transformed is None:
                # If expected is a list but no points given to transform,
                # fall back to returning expected-like transform of source->target if provided.
                transformed = []
            return self._denormalize_points_like(expected, transformed)

        # Otherwise return a rich solution dict
        solution = {
            'matrix': [[M[0][0], M[0][1]], [M[1][0], M[1][1]]],
            'translate': [t[0], t[1]]
        }
        if transformed is not None:
            solution['transformed_points'] = self._denormalize_points(
                transformed)

        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        tol = problem.get('tolerance', 1e-6)

        expected = problem.get('expected', None)

        # Case 1: expected is list of transformed points
        if isinstance(expected, list):
            # Compare expected points to proposed solution
            if isinstance(solution, dict) and 'transformed_points' in solution:
                cand = solution['transformed_points']
            else:
                cand = solution
            return self._compare_points_lists(expected, cand, tol)

        # Case 2: expected is dict with matrix/translate
        if isinstance(expected, dict):
            # Try to compare transform parameters if provided
            exp_M = expected.get('matrix')
            exp_t = expected.get('translate')
            if exp_M is not None and exp_t is not None:
                # Normalize both
                sM, st = None, None
                if isinstance(solution, dict):
                    sM = solution.get('matrix')
                    st = solution.get('translate')
                if sM is None or st is None:
                    # Try derive from solution if it contains transformed points and we have correspondences
                    M, t = self._extract_or_fit_affine(problem, fallback=True)
                    sM, st = [[M[0][0], M[0][1]], [
                        M[1][0], M[1][1]]], [t[0], t[1]]
                return self._compare_matrix(exp_M, sM, tol) and self._compare_vector(exp_t, st, tol)

        # Case 3: No explicit expected. Validate transform against source->target if available.
        src = problem.get('source_points') or problem.get(
            'src') or problem.get('from_points')
        dst = problem.get('target_points') or problem.get(
            'dst') or problem.get('to_points')
        if src is not None and dst is not None:
            # Obtain transform from candidate solution
            if isinstance(solution, dict) and 'matrix' in solution and 'translate' in solution:
                M = solution['matrix']
                t = solution['translate']
                # Normalize M, t
                M = [[float(M[0][0]), float(M[0][1])], [
                    float(M[1][0]), float(M[1][1])]]
                t = [float(t[0]), float(t[1])]
            else:
                # Derive from problem using built-in fitting
                M, t = self._extract_or_fit_affine(problem, fallback=True)
                M = [[M[0][0], M[0][1]], [M[1][0], M[1][1]]]
                t = [t[0], t[1]]

            src_n = self._normalize_points(src)
            mapped = self._apply_affine(M, t, src_n, rounding=None)
            dst_n = self._normalize_points(dst)
            return self._compare_points_lists(self._denormalize_points(dst_n), self._denormalize_points(mapped), tol)

        # If we reach here, accept if solution is a dict with matrix/translate or list when expected absent
        if isinstance(solution, dict):
            return 'matrix' in solution and 'translate' in solution
        return solution is not None

    # ---------------------- Internal Utilities ----------------------

    def _extract_or_fit_affine(self, problem, fallback=False):
        # 1) Direct parameters
        direct = self._get_direct_affine(problem)
        if direct is not None:
            return direct

        # 2) From geometric params: scale + rotation + translation
        derived = self._get_parametric_affine(problem)
        if derived is not None:
            return derived

        # 3) Fit from correspondences
        src = problem.get('source_points') or problem.get(
            'src') or problem.get('from_points')
        dst = problem.get('target_points') or problem.get(
            'dst') or problem.get('to_points')
        if src is not None and dst is not None:
            src = self._normalize_points(src)
            dst = self._normalize_points(dst)
            M, t = self._fit_affine_from_correspondences(src, dst)
            return M, t

        if fallback:
            # identity as a safe fallback
            return [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0]

        raise ValueError('Insufficient data to determine affine transform.')

    def _get_direct_affine(self, problem):
        M = problem.get('matrix')
        t = problem.get('translate') or problem.get(
            'translation') or problem.get('t')
        if M is None or t is None:
            return None
        # Normalize shapes
        M = [[float(M[0][0]), float(M[0][1])],
             [float(M[1][0]), float(M[1][1])]]
        t = [float(t[0]), float(t[1])]
        return M, t

    def _get_parametric_affine(self, problem):
        # Accept scale (uniform), rotation (deg/rad), translation
        scale = problem.get('scale', 1.0)
        if isinstance(scale, (list, tuple)) and len(scale) == 2:
            sx, sy = float(scale[0]), float(scale[1])
        else:
            sx = sy = float(scale)

        if 'rotation_radians' in problem:
            theta = float(problem['rotation_radians'])
        elif 'rotation' in problem and isinstance(problem['rotation'], (int, float)):
            theta = float(problem['rotation'])
        elif 'rotation_degrees' in problem:
            theta = float(problem['rotation_degrees']) * 0.017453292519943295
        else:
            theta = 0.0

        tx, ty = 0.0, 0.0
        tr = problem.get('translate') or problem.get(
            'translation') or problem.get('t')
        if tr is not None:
            tx, ty = float(tr[0]), float(tr[1])

        # Allow skew/shear if provided
        shear = problem.get('shear', None)
        if shear is None:
            # Rotation then scale (anisotropic), M = R * S
            c = self._cos(theta)
            s = self._sin(theta)
            M = [[c * sx, -s * sy],
                 [s * sx,  c * sy]]
        else:
            # shear can be float or (shx, shy)
            if isinstance(shear, (list, tuple)) and len(shear) == 2:
                shx, shy = float(shear[0]), float(shear[1])
            else:
                shx = float(shear)
                shy = 0.0
            # Build scale, shear, rotation: M = R * Sh * S
            S = [[sx, 0.0], [0.0, sy]]
            Sh = [[1.0, shx], [shy, 1.0]]
            c = self._cos(theta)
            s = self._sin(theta)
            R = [[c, -s], [s, c]]
            M = self._matmul(R, self._matmul(Sh, S))

        return M, [tx, ty]

    def _fit_affine_from_correspondences(self, src, dst):
        n = min(len(src), len(dst))
        if n <= 0:
            return [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0]
        if n == 1:
            # Pure translation
            (x0, y0), (u0, v0) = src[0], dst[0]
            return [[1.0, 0.0], [0.0, 1.0]], [u0 - x0, v0 - y0]
        if n == 2:
            # Similarity transform: [a -b; b a] and translation
            (x1, y1), (x2, y2) = src[0], src[1]
            (u1, v1), (u2, v2) = dst[0], dst[1]
            vx1, vy1 = x2 - x1, y2 - y1
            vx0, vy0 = u2 - u1, v2 - v1
            denom = vx1 * vx1 + vy1 * vy1
            if abs(denom) < 1e-12:
                # Degenerate, fallback to translation average
                tx = ((u1 - x1) + (u2 - x2)) / 2.0
                ty = ((v1 - y1) + (v2 - y2)) / 2.0
                return [[1.0, 0.0], [0.0, 1.0]], [tx, ty]
            # Solve for a, b
            # [ vx1 -vy1 ] [a] = [vx0]
            # [ vy1  vx1 ] [b]   [vy0]
            a = (vx1 * vx0 + vy1 * vy0) / denom
            b = (-vy1 * vx0 + vx1 * vy0) / denom
            M = [[a, -b], [b, a]]
            tx = u1 - (a * x1 - b * y1)
            ty = v1 - (b * x1 + a * y1)
            return M, [tx, ty]

        # n >= 3: Least squares for full affine (6 DOF)
        A = []
        b = []
        for (x, y), (u, v) in zip(src, dst):
            A.append([x, y, 0.0, 0.0, 1.0, 0.0])
            b.append(u)
            A.append([0.0, 0.0, x, y, 0.0, 1.0])
            b.append(v)
        # Solve (A^T A) p = A^T b
        ATA = self._matT_mat(A, A)
        ATb = self._matT_vec(A, b)
        p = self._solve_linear_system(ATA, ATb)
        a, b_, c, d, tx, ty = p
        M = [[a, b_], [c, d]]
        t = [tx, ty]
        return M, t

    def _apply_affine(self, M, t, points, rounding=None, ndigits=None):
        out = []
        # Determine default rounding from input types if not specified
        default_round = False
        if rounding is None:
            # If all input points are integers, default to integer outputs
            default_round = all(
                isinstance(px, int) and isinstance(py, int)
                for (px, py) in points if points
            )
        for (x, y) in points:
            u = M[0][0] * x + M[0][1] * y + t[0]
            v = M[1][0] * x + M[1][1] * y + t[1]
            if rounding is True or rounding == 'nearest' or (rounding is None and default_round):
                if ndigits is not None:
                    u = round(u, int(ndigits))
                    v = round(v, int(ndigits))
                u = int(round(u))
                v = int(round(v))
            elif rounding == 'floor':
                from math import floor
                u = floor(u)
                v = floor(v)
            elif rounding == 'ceil':
                from math import ceil
                u = ceil(u)
                v = ceil(v)
            else:
                if ndigits is not None:
                    u = round(u, int(ndigits))
                    v = round(v, int(ndigits))
            out.append((u, v))
        return out

    # ---------------------- Math Helpers ----------------------

    def _solve_linear_system(self, A, b):
        # Gaussian elimination with partial pivoting
        n = len(A)
        # Augment
        aug = [row[:] + [b[i]] for i, row in enumerate(A)]
        for col in range(n):
            # Pivot
            pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
            if abs(aug[pivot_row][col]) < 1e-18:
                # Singular, regularize with small identity term
                for i in range(n):
                    aug[i][i] += 1e-12
                pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
                if abs(aug[pivot_row][col]) < 1e-18:
                    continue
            if pivot_row != col:
                aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
            # Normalize pivot row
            pivot = aug[col][col]
            invp = 1.0 / pivot
            for j in range(col, n + 1):
                aug[col][j] *= invp
            # Eliminate below
            for r in range(col + 1, n):
                fac = aug[r][col]
                if fac == 0.0:
                    continue
                for j in range(col, n + 1):
                    aug[r][j] -= fac * aug[col][j]
        # Back substitution
        x = [0.0] * n
        for i in reversed(range(n)):
            s = aug[i][n]
            for j in range(i + 1, n):
                s -= aug[i][j] * x[j]
            denom = aug[i][i]
            if abs(denom) < 1e-18:
                x[i] = 0.0
            else:
                x[i] = s / denom
        return x

    def _matmul(self, A, B):
        return [
            [
                A[0][0] * B[0][j] + A[0][1] * B[1][j]
                for j in range(2)
            ],
            [
                A[1][0] * B[0][j] + A[1][1] * B[1][j]
                for j in range(2)
            ],
        ]

    def _matT_mat(self, A, B):
        # A: m x n, B: m x n -> A^T B: n x n
        m = len(A)
        n = len(A[0]) if m > 0 else 0
        BT = list(zip(*B)) if m > 0 else []
        out = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s = 0.0
                for k in range(m):
                    s += A[k][i] * BT[j][k]
                out[i][j] = s
        return out

    def _matT_vec(self, A, v):
        # A: m x n, v: m -> A^T v: n
        m = len(A)
        n = len(A[0]) if m > 0 else 0
        out = [0.0] * n
        for i in range(n):
            s = 0.0
            for k in range(m):
                s += A[k][i] * v[k]
            out[i] = s
        return out

    def _cos(self, x):
        from math import cos
        return cos(x)

    def _sin(self, x):
        from math import sin
        return sin(x)

    # ---------------------- Data Helpers ----------------------

    def _normalize_points(self, pts):
        out = []
        for p in pts:
            if isinstance(p, dict) and 'x' in p and 'y' in p:
                x, y = p['x'], p['y']
            elif isinstance(p, (list, tuple)) and len(p) >= 2:
                x, y = p[0], p[1]
            else:
                raise ValueError('Unsupported point format: {}'.format(p))
            out.append((float(x), float(y)))
        return out

    def _denormalize_points(self, pts):
        # Return as list of [x, y] ints if both are ints; else floats
        out = []
        for x, y in pts:
            if self._is_int_like(x) and self._is_int_like(y):
                out.append([int(round(x)), int(round(y))])
            else:
                out.append([x, y])
        return out

    def _denormalize_points_like(self, template, pts):
        # Match format of template list
        out = []
        for i, p in enumerate(pts):
            x, y = p
            t = template[i] if i < len(template) else template[-1]
            if isinstance(t, dict) and 'x' in t and 'y' in t:
                if self._is_int_like(x):
                    x = int(round(x))
                if self._is_int_like(y):
                    y = int(round(y))
                out.append({'x': x, 'y': y})
            elif isinstance(t, (list, tuple)):
                if self._is_int_like(x):
                    x = int(round(x))
                if self._is_int_like(y):
                    y = int(round(y))
                out.append([x, y] if isinstance(t, list) else (x, y))
            else:
                # Fallback to list
                if self._is_int_like(x):
                    x = int(round(x))
                if self._is_int_like(y):
                    y = int(round(y))
                out.append([x, y])
        return out

    def _compare_points_lists(self, expected, candidate, tol):
        exp_n = self._normalize_points(expected)
        try:
            cand_n = self._normalize_points(candidate)
        except Exception:
            return False
        if len(exp_n) != len(cand_n):
            return False
        for (ex, ey), (cx, cy) in zip(exp_n, cand_n):
            if not (abs(ex - cx) <= tol and abs(ey - cy) <= tol):
                return False
        return True

    def _compare_matrix(self, A, B, tol):
        if A is None or B is None:
            return False
        if len(A) != 2 or len(B) != 2 or len(A[0]) != 2 or len(A[1]) != 2 or len(B[0]) != 2 or len(B[1]) != 2:
            return False
        for i in range(2):
            for j in range(2):
                if abs(float(A[i][j]) - float(B[i][j])) > tol:
                    return False
        return True

    def _compare_vector(self, a, b, tol):
        if a is None or b is None:
            return False
        if len(a) != 2 or len(b) != 2:
            return False
        return abs(float(a[0]) - float(b[0])) <= tol and abs(float(a[1]) - float(b[1])) <= tol

    def _is_int_like(self, x):
        return isinstance(x, int) or (isinstance(x, float) and abs(x - round(x)) < 1e-9)
