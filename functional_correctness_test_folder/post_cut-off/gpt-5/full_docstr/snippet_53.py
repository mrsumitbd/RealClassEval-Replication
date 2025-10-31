class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Build transform matrix (3x3 homogeneous)
        M = None
        if 'matrix' in problem and problem['matrix'] is not None:
            M = self._to_3x3(problem['matrix'])
        else:
            M = self._build_from_params(
                translation=problem.get('translation'),
                rotation=problem.get('rotation'),
                scale=problem.get('scale'),
                shear=problem.get('shear'),
                center=problem.get('center')
            )

        # Rounding behavior
        round_to_int = bool(problem.get('round', False))
        precision = problem.get('precision', None)

        if 'points' in problem and problem['points'] is not None:
            pts = problem['points']
            out = []
            for p in pts:
                x, y = p
                x2, y2, w = self._mat_vec_mul(M, [x, y, 1.0])
                if w != 0:
                    x2, y2 = x2 / w, y2 / w
                if round_to_int:
                    if precision is None:
                        x2, y2 = int(round(x2)), int(round(y2))
                    else:
                        x2, y2 = round(x2, int(precision)), round(
                            y2, int(precision))
                out.append([x2, y2])
            return out

        if 'image' in problem and problem['image'] is not None:
            img = problem['image']
            h = len(img) if isinstance(img, list) else 0
            w = len(img[0]) if h > 0 and isinstance(img[0], list) else 0
            out_h, out_w = problem.get('output_size', (h, w))
            background = problem.get('background', 0)
            # Compute inverse for backward mapping
            Minv = self._invert_3x3(M)
            # Optional origin offset
            origin = problem.get('origin', (0.0, 0.0))
            ox, oy = origin if origin else (0.0, 0.0)

            out_img = [[background for _ in range(
                out_w)] for _ in range(out_h)]
            for yy in range(out_h):
                for xx in range(out_w):
                    # Map output pixel center to input coordinates
                    x_in, y_in, w_in = self._mat_vec_mul(
                        Minv, [xx + ox, yy + oy, 1.0])
                    if w_in != 0:
                        x_in, y_in = x_in / w_in, y_in / w_in
                    # nearest neighbor
                    xi = int(round(x_in))
                    yi = int(round(y_in))
                    if 0 <= yi < h and 0 <= xi < w:
                        out_img[yy][xx] = img[yi][xi]
                    else:
                        out_img[yy][xx] = background
            return out_img

        # If no recognizable inputs, return None
        return None

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        expected = problem.get('expected', None)
        if expected is None:
            # If no expected provided, validate by recomputation equivalence
            recomputed = self.solve(problem)
            return self._equal_structures(recomputed, solution)
        # Compare to expected
        return self._equal_structures(expected, solution)

    # ----------------- Helpers -----------------

    def _to_3x3(self, M):
        # Accept 2x3, 3x3, flat lengths 6 or 9
        if isinstance(M, (list, tuple)):
            # Flatten detection
            if all(isinstance(r, (int, float)) for r in M):
                if len(M) == 6:
                    a, b, c, d, e, f = M
                    return [[a, b, c],
                            [d, e, f],
                            [0.0, 0.0, 1.0]]
                if len(M) == 9:
                    return [list(M[0:3]), list(M[3:6]), list(M[6:9])]
            # 2D list
            if len(M) == 2 and len(M[0]) == 3 and len(M[1]) == 3:
                return [list(M[0]), list(M[1]), [0.0, 0.0, 1.0]]
            if len(M) == 3 and len(M[0]) == 3 and len(M[1]) == 3 and len(M[2]) == 3:
                return [list(M[0]), list(M[1]), list(M[2])]
        raise ValueError("Unsupported matrix format for affine transform")

    def _build_from_params(self, translation=None, rotation=None, scale=None, shear=None, center=None):
        # Start with identity
        M = self._identity_3()
        # Centering: translate to center, apply, translate back
        pre = self._identity_3()
        post = self._identity_3()
        if center is not None:
            cx, cy = center
            pre = self._translation_3(-cx, -cy)
            post = self._translation_3(cx, cy)

        # Compose in standard order: Scale -> Shear -> Rotate -> Translate
        C = self._identity_3()

        if scale is not None:
            if isinstance(scale, (int, float)):
                sx = sy = float(scale)
            else:
                sx = float(scale[0])
                sy = float(scale[1])
            C = self._mat_mul(self._scale_3(sx, sy), C)

        if shear is not None:
            # shear can be float or tuple (shx, shy) in radians or degrees if 'shear_degrees' set
            if isinstance(shear, (int, float)):
                shx = float(shear)
                shy = 0.0
            else:
                shx = float(shear[0])
                shy = float(shear[1])
            if isinstance(shear, (int, float)) or isinstance(shear[0], (int, float)):
                # Assume radians by default; check flag
                if self._flag_true("shear_degrees", False):
                    shx = self._deg2rad(shx)
                    shy = self._deg2rad(shy)
            C = self._mat_mul(self._shear_3(shx, shy), C)

        if rotation is not None:
            ang = float(rotation)
            # By default, assume degrees unless rotation_radians True
            use_radians = self._flag_true("rotation_radians", False)
            if not use_radians:
                ang = self._deg2rad(ang)
            C = self._mat_mul(self._rotation_3(ang), C)

        if translation is not None:
            tx, ty = float(translation[0]), float(translation[1])
            C = self._mat_mul(self._translation_3(tx, ty), C)

        M = self._mat_mul(post, self._mat_mul(C, pre))
        return M

    def _flag_true(self, key, default):
        # Placeholder for potential environment flags; always return default here.
        return default

    def _identity_3(self):
        return [[1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]]

    def _translation_3(self, tx, ty):
        return [[1.0, 0.0, float(tx)],
                [0.0, 1.0, float(ty)],
                [0.0, 0.0, 1.0]]

    def _scale_3(self, sx, sy):
        return [[float(sx), 0.0, 0.0],
                [0.0, float(sy), 0.0],
                [0.0, 0.0, 1.0]]

    def _rotation_3(self, theta):
        import math
        c = math.cos(theta)
        s = math.sin(theta)
        return [[c, -s, 0.0],
                [s,  c, 0.0],
                [0.0, 0.0, 1.0]]

    def _shear_3(self, shx, shy):
        # Shear matrix with shx along x due to y, and shy along y due to x
        return [[1.0, float(shx), 0.0],
                [float(shy), 1.0, 0.0],
                [0.0, 0.0, 1.0]]

    def _deg2rad(self, deg):
        import math
        return deg * math.pi / 180.0

    def _mat_mul(self, A, B):
        # 3x3 * 3x3
        out = [[0.0, 0.0, 0.0] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                s = 0.0
                for k in range(3):
                    s += A[i][k] * B[k][j]
                out[i][j] = s
        return out

    def _mat_vec_mul(self, A, v):
        # 3x3 * 3x1
        return [
            A[0][0] * v[0] + A[0][1] * v[1] + A[0][2] * v[2],
            A[1][0] * v[0] + A[1][1] * v[1] + A[1][2] * v[2],
            A[2][0] * v[0] + A[2][1] * v[1] + A[2][2] * v[2],
        ]

    def _invert_3x3(self, M):
        # General 3x3 inverse
        a, b, c = M[0]
        d, e, f = M[1]
        g, h, i = M[2]
        A = e * i - f * h
        B = -(d * i - f * g)
        C = d * h - e * g
        D = -(b * i - c * h)
        E = a * i - c * g
        F = -(a * h - b * g)
        G = b * f - c * e
        H = -(a * f - c * d)
        I = a * e - b * d
        det = a * A + b * B + c * C
        if det == 0:
            raise ValueError("Singular matrix cannot be inverted")
        inv_det = 1.0 / det
        return [
            [A * inv_det, D * inv_det, G * inv_det],
            [B * inv_det, E * inv_det, H * inv_det],
            [C * inv_det, F * inv_det, I * inv_det],
        ]

    def _equal_structures(self, a, b, tol=1e-6):
        # Compare nested structures with tolerance for floats
        if type(a) != type(b):
            return False
        if isinstance(a, (int, float)):
            if isinstance(a, float) or isinstance(b, float):
                return abs(float(a) - float(b)) <= tol
            return a == b
        if isinstance(a, list):
            if len(a) != len(b):
                return False
            for x, y in zip(a, b):
                if not self._equal_structures(x, y, tol):
                    return False
            return True
        if isinstance(a, tuple):
            if len(a) != len(b):
                return False
            for x, y in zip(a, b):
                if not self._equal_structures(x, y, tol):
                    return False
            return True
        if isinstance(a, dict):
            if a.keys() != b.keys():
                return False
            for k in a:
                if not self._equal_structures(a[k], b[k], tol):
                    return False
            return True
        return a == b
