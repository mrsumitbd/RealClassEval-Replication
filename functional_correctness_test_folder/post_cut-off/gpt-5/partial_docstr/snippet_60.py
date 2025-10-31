class PolynomialReal:

    def __init__(self):
        self.tol = 1e-8

    def _normalize_coeffs(self, coeffs):
        if not isinstance(coeffs, (list, tuple)):
            raise ValueError("coefficients must be a list or tuple")
        coeffs = [float(c) for c in coeffs]
        # Remove leading zeros
        i = 0
        while i < len(coeffs) and abs(coeffs[i]) <= self.tol:
            i += 1
        coeffs = coeffs[i:] if i < len(coeffs) else [0.0]
        return coeffs

    def _poly_eval(self, coeffs, x):
        # coeffs are in descending powers
        val = 0.0
        for c in coeffs:
            val = val * x + c
        return val

    def _quad_roots(self, a, b, c):
        # ax^2 + bx + c = 0
        if abs(a) <= self.tol:
            # degrade to linear
            if abs(b) <= self.tol:
                return []
            return [-c / b]
        disc = b * b - 4.0 * a * c
        if disc < -self.tol:
            return []
        elif abs(disc) <= self.tol:
            r = -b / (2.0 * a)
            return [r]
        else:
            sqrt_disc = disc ** 0.5
            # Numerically stable quadratic formula
            if b >= 0:
                q = -0.5 * (b + sqrt_disc)
            else:
                q = -0.5 * (b - sqrt_disc)
            r1 = q / a
            r2 = c / q if abs(q) > self.tol else -b / a - r1
            return [r1, r2]

    def _unique_sorted(self, roots):
        # Merge roots that are within tolerance and sort
        roots_sorted = sorted(roots)
        merged = []
        for r in roots_sorted:
            if not merged:
                merged.append(r)
            elif abs(r - merged[-1]) <= self.tol * max(1.0, abs(r), abs(merged[-1])):
                # average close roots
                merged[-1] = (merged[-1] + r) / 2.0
            else:
                merged.append(r)
        return merged

    def _real_roots_via_numpy(self, coeffs):
        try:
            import numpy as np
        except Exception:
            return None
        c = np.array(coeffs, dtype=np.complex128)
        if c.size == 1:
            return []
        roots = np.roots(c)
        real_roots = []
        for z in roots:
            if abs(z.imag) <= self.tol:
                real_roots.append(float(z.real))
        return self._unique_sorted(real_roots)

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        # Accept common keys
        coeffs = (
            problem.get("coefficients")
            or problem.get("coeffs")
            or problem.get("poly")
        )
        if coeffs is None:
            raise ValueError(
                "Problem must contain 'coefficients' (descending powers)")
        order = problem.get("order", "descending")
        coeffs = list(coeffs)
        if order == "ascending":
            coeffs = list(reversed(coeffs))
        coeffs = self._normalize_coeffs(coeffs)

        # Degree checks
        if len(coeffs) == 1:
            c0 = coeffs[0]
            if abs(c0) <= self.tol:
                return {"type": "all_real"}
            else:
                return []

        deg = len(coeffs) - 1

        # Linear
        if deg == 1:
            a, b = coeffs
            if abs(a) <= self.tol:
                # Degenerate to constant
                if abs(b) <= self.tol:
                    return {"type": "all_real"}
                else:
                    return []
            root = -b / a
            return [root]

        # Quadratic
        if deg == 2:
            a, b, c = coeffs
            roots = self._quad_roots(a, b, c)
            roots = [r for r in roots if abs(self._poly_eval(coeffs, r)) <= max(
                self.tol, self.tol * (abs(r) + 1.0))]
            return self._unique_sorted(roots)

        # Higher degree: use numpy if available
        roots = self._real_roots_via_numpy(coeffs)
        if roots is None:
            # Fallback: no reliable general solver without numpy; return empty
            return []
        # Validate roots by evaluation
        filtered = []
        for r in roots:
            if abs(self._poly_eval(coeffs, r)) <= max(self.tol, self.tol * (abs(r) + 1.0)):
                filtered.append(r)
        return self._unique_sorted(filtered)

    def is_solution(self, problem, solution):
        # Validate structure first
        coeffs = (
            problem.get("coefficients")
            or problem.get("coeffs")
            or problem.get("poly")
        )
        if coeffs is None:
            return False
        order = problem.get("order", "descending")
        coeffs = list(coeffs)
        if order == "ascending":
            coeffs = list(reversed(coeffs))
        coeffs = self._normalize_coeffs(coeffs)

        expected = self.solve(problem)

        # Handle all real case
        if isinstance(expected, dict) and expected.get("type") == "all_real":
            return isinstance(solution, dict) and solution.get("type") == "all_real"

        # Expected list
        if not isinstance(solution, (list, tuple)):
            return False
        try:
            sol_roots = [float(x) for x in solution]
        except Exception:
            return False

        # Clean both sets
        exp_roots = expected if isinstance(expected, list) else []
        exp_roots = self._unique_sorted(exp_roots)
        sol_roots = self._unique_sorted(sol_roots)

        # Length must match
        if len(exp_roots) != len(sol_roots):
            return False

        # Pairwise closeness
        for a, b in zip(exp_roots, sol_roots):
            if abs(a - b) > self.tol * max(1.0, abs(a), abs(b)):
                return False
            # Additionally verify solution roots satisfy polynomial
            if abs(self._poly_eval(coeffs, b)) > max(self.tol, self.tol * (abs(b) + 1.0)):
                return False

        return True
