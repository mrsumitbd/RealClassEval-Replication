class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        pass

    def _strip_leading_zeros(self, coeffs):
        i = 0
        n = len(coeffs)
        while i < n and abs(coeffs[i]) == 0:
            i += 1
        if i == n:
            return [0.0]
        return [float(c) for c in coeffs[i:]]

    def _poly_eval(self, coeffs, x):
        # Horner's method
        res = 0.0 + 0.0j if isinstance(x, complex) else 0.0
        for c in coeffs:
            res = res * x + c
        return res

    def _durand_kerner(self, coeffs, max_iter=1000, tol=1e-14):
        # coeffs in descending order. Assumes degree >= 1.
        # Normalize to monic
        lc = coeffs[0]
        if lc == 0:
            raise ValueError("Leading coefficient cannot be zero.")
        coeffs_monic = [c / lc for c in coeffs]
        n = len(coeffs_monic) - 1  # degree

        # Initial guesses: distinct points on a circle
        import cmath
        radius = 1.0
        roots = [radius * cmath.exp(2j * cmath.pi * k / n) for k in range(n)]

        for _ in range(max_iter):
            converged = True
            new_roots = []
            for i in range(n):
                xi = roots[i]
                # Evaluate polynomial at xi
                px = self._poly_eval(coeffs_monic, xi)
                # Compute denominator: product (xi - xj) for j != i
                denom = 1.0 + 0.0j
                for j in range(n):
                    if i != j:
                        denom *= (xi - roots[j])
                if denom == 0:
                    # Slight perturbation to avoid division by zero
                    xi += (1e-12 + 1e-12j)
                    denom = 1.0 + 0.0j
                    for j in range(n):
                        if i != j:
                            denom *= (xi - roots[j])
                delta = px / denom
                xnew = xi - delta
                new_roots.append(xnew)
                if abs(xnew - xi) > tol:
                    converged = False
            roots = new_roots
            if converged:
                break
        return roots

    def _real_roots(self, coeffs, tol_imag=1e-8, tol_merge=1e-6):
        coeffs = self._strip_leading_zeros(coeffs)
        # Handle degree cases
        if len(coeffs) == 1:
            # constant polynomial
            if coeffs[0] == 0:
                # Identically zero: infinite roots; return empty as convention
                return {"type": "infinite", "roots": []}
            else:
                return {"type": "finite", "roots": []}
        if len(coeffs) == 2:
            # linear ax + b = 0
            a, b = coeffs
            if a == 0:
                # degenerate handled above but just in case
                return {"type": "finite", "roots": []}
            root = -b / a
            return {"type": "finite", "roots": [float(root)]}

        # General case: numeric roots
        complex_roots = self._durand_kerner(coeffs)
        real_roots = []
        for r in complex_roots:
            if abs(r.imag) <= tol_imag:
                real_roots.append(r.real)

        if not real_roots:
            return {"type": "finite", "roots": []}

        # Merge near-duplicates (handle multiplicities with tolerance)
        real_roots.sort()
        merged = []
        current = real_roots[0]
        count = 1
        for x in real_roots[1:]:
            if abs(x - current) <= tol_merge:
                # Average within cluster
                current = (current * count + x) / (count + 1)
                count += 1
            else:
                merged.append(current)
                current = x
                count = 1
        merged.append(current)

        return {"type": "finite", "roots": [float(r) for r in merged]}

    def _extract_coeffs(self, problem):
        # Try multiple keys for flexibility
        keys = ["coefficients", "coefs", "poly", "polynomial"]
        coeffs = None
        for k in keys:
            if k in problem:
                coeffs = problem[k]
                break
        if coeffs is None:
            raise ValueError(
                "Problem must include coefficients under one of: coefficients, coefs, poly, polynomial")
        if not isinstance(coeffs, (list, tuple)) or len(coeffs) == 0:
            raise ValueError("Coefficients must be a non-empty list/tuple")
        # Ensure numeric
        try:
            coeffs = [float(c) for c in coeffs]
        except Exception as e:
            raise ValueError("Coefficients must be numeric") from e
        return coeffs

    def _normalize_solution_input(self, solution):
        # Accept either list of numbers or dict with 'roots'
        if isinstance(solution, dict):
            if "roots" in solution:
                solution = solution["roots"]
            else:
                return None
        if solution is None:
            return None
        if not isinstance(solution, (list, tuple)):
            return None
        nums = []
        for x in solution:
            try:
                if isinstance(x, complex):
                    nums.append(float(x.real))
                else:
                    nums.append(float(x))
            except Exception:
                return None
        return nums

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        coeffs = self._extract_coeffs(problem)
        res = self._real_roots(coeffs)
        # Return standardized format: list of real roots sorted ascending
        # If infinite roots, return empty list to indicate special case
        if res["type"] == "infinite":
            return []
        return sorted(res["roots"])

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        tol = problem.get(
            "tolerance", 1e-5) if isinstance(problem, dict) else 1e-5
        coeffs = self._extract_coeffs(problem)

        ground = self._real_roots(coeffs)
        user_roots = self._normalize_solution_input(solution)
        if user_roots is None:
            return False

        if ground["type"] == "infinite":
            return True

        # Sort both and compare with tolerance, accounting for multiplicity as unique merged roots
        def merge(vals, tol_merge):
            if not vals:
                return []
            vals = sorted(vals)
            merged = [vals[0]]
            for x in vals[1:]:
                if abs(x - merged[-1]) <= tol_merge:
                    # average
                    merged[-1] = 0.5 * (merged[-1] + x)
                else:
                    merged.append(x)
            return merged

        user_m = merge(user_roots, tol)
        gold_m = merge(ground["roots"], tol)

        if len(user_m) != len(gold_m):
            return False

        for a, b in zip(sorted(user_m), sorted(gold_m)):
            if abs(a - b) > tol:
                return False

        return True
