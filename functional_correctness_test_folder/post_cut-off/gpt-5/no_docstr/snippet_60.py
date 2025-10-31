class PolynomialReal:

    def __init__(self, tol=1e-9, max_iter=1000):
        self.tol = float(tol)
        self.max_iter = int(max_iter)

    def _parse_problem(self, problem):
        # Acceptable formats:
        # - dict with key 'coefficients'
        # - list/tuple of numbers
        # - string of space- or comma-separated numbers
        coeffs = None
        if isinstance(problem, dict):
            if 'coefficients' in problem:
                coeffs = problem['coefficients']
            else:
                raise ValueError("Problem dict must contain 'coefficients'.")
        elif isinstance(problem, (list, tuple)):
            coeffs = problem
        elif isinstance(problem, str):
            # Try to parse comma/space separated numbers
            raw = problem.replace(',', ' ').split()
            coeffs = [float(x) for x in raw]
        else:
            raise TypeError("Unsupported problem format.")

        # Convert to list of floats
        try:
            coeffs = [float(x) for x in coeffs]
        except Exception as e:
            raise ValueError("Coefficients must be numeric.") from e

        # Strip leading zeros
        i = 0
        while i < len(coeffs) and abs(coeffs[i]) <= self.tol:
            i += 1
        coeffs = coeffs[i:] if i < len(coeffs) else [0.0]

        return coeffs

    def _poly_eval(self, coeffs, x):
        # Horner's method; coeffs in descending powers
        y = 0.0 + 0.0j
        for c in coeffs:
            y = y * x + c
        return y

    def _quadratic_roots_real(self, a, b, c):
        import math
        if abs(a) <= self.tol:
            if abs(b) <= self.tol:
                return []
            return [(-c) / b]
        disc = b * b - 2 * 2 * a * c  # b^2 - 4ac
        if disc < 0 and abs(disc) <= self.tol:
            disc = 0.0
        if disc < 0:
            return []
        sqrt_disc = math.sqrt(disc)
        # Use numerically stable quadratic formula
        if b >= 0:
            q = -0.5 * (b + sqrt_disc)
        else:
            q = -0.5 * (b - sqrt_disc)
        if abs(a) > self.tol:
            r1 = q / a
        else:
            r1 = float('nan')
        r2 = c / q if abs(q) > self.tol else r1
        roots = []
        for r in (r1, r2):
            if isinstance(r, float) and (not math.isfinite(r)):
                continue
            roots.append(r)
        roots.sort()
        return roots

    def _durand_kerner(self, coeffs):
        # Find all complex roots using Durand-Kerner method
        # coeffs in descending powers, degree >= 1
        import cmath
        n = len(coeffs) - 1
        a0 = coeffs[0]
        if abs(a0) <= self.tol:
            raise ValueError(
                "Leading coefficient must be non-zero after normalization.")
        # Normalize to monic
        monic = [c / a0 for c in coeffs]
        # Initial guesses on a circle
        # Radius heuristic: 1 + max(|c|) for stability
        radius = 1.0 + max(abs(c) for c in monic[1:]) if n > 0 else 1.0
        roots = [radius * cmath.exp(2j * cmath.pi * k / n) for k in range(n)]
        for _ in range(self.max_iter):
            converged = True
            new_roots = []
            for i in range(n):
                zi = roots[i]
                # Evaluate polynomial (monic)
                p = monic[0]
                for c in monic[1:]:
                    p = p * zi + c
                denom = 1.0 + 0.0j
                for j in range(n):
                    if i == j:
                        continue
                    diff = zi - roots[j]
                    # If too close, jitter slightly
                    if abs(diff) < 1e-14:
                        diff = diff + (1e-8 + 1e-8j)
                    denom *= diff
                if abs(denom) <= 0:
                    denom = 1e-12 + 0j
                delta = p / denom
                zi_new = zi - delta
                new_roots.append(zi_new)
                if abs(delta) > self.tol:
                    converged = False
            roots = new_roots
            if converged:
                break
        return roots

    def _unique_sorted_reals(self, vals):
        vals = sorted(vals)
        unique = []
        for v in vals:
            if not unique:
                unique.append(v)
            else:
                if abs(v - unique[-1]) > 1e-7:
                    unique.append(v)
        return unique

    def solve(self, problem):
        coeffs = self._parse_problem(problem)
        # Degree
        deg = len(coeffs) - 1

        # Constant polynomial
        if deg == 0:
            # ax^0 = c; if c != 0 -> no roots; if c == 0 -> all real numbers (indeterminate)
            return []

        # Linear: a x + b = 0
        if deg == 1:
            a, b = coeffs
            if abs(a) <= self.tol:
                return []  # Degenerate to constant non-zero likely handled before
            return [(-b) / a]

        # Quadratic
        if deg == 2:
            a, b, c = coeffs
            return self._quadratic_roots_real(a, b, c)

        # Higher degree: Durand-Kerner to find complex roots, then keep real ones
        roots_c = self._durand_kerner(coeffs)
        reals = []
        for z in roots_c:
            if abs(z.imag) <= 1e-7:
                reals.append(z.real)
        reals = self._unique_sorted_reals(reals)
        return reals

    def is_solution(self, problem, solution):
        coeffs = self._parse_problem(problem)
        # Normalize solution input
        if solution is None:
            return False
        if isinstance(solution, (int, float)):
            sols = [float(solution)]
        elif isinstance(solution, (list, tuple)):
            sols = []
            for s in solution:
                if isinstance(s, (int, float)):
                    sols.append(float(s))
                else:
                    return False
        else:
            return False

        # Evaluate each candidate solution; must be real and satisfy P(x)=0 within tolerance
        # Scale-aware tolerance based on polynomial value magnitude
        def residual_ok(x):
            px = self._poly_eval(coeffs, complex(x, 0.0))
            scale = 0.0
            # Compute simple bound sum |c_i| |x|^i
            p = 0.0
            for k, c in enumerate(reversed(coeffs)):
                # reversed: constant first; degree increases with k
                p = p * abs(x) + abs(c)
            scale = max(1.0, p)
            return abs(px) <= self.tol * scale

        for x in sols:
            if not (isinstance(x, float) or isinstance(x, int)):
                return False
            # Check finiteness
            if not (float('-inf') < float(x) < float('inf')):
                return False
            if not residual_ok(float(x)):
                return False
        return True
