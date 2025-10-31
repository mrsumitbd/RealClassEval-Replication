
import math


class PolynomialReal:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
                {
                    "coefficients": [a_n, ..., a_0]  # list of real coefficients, highest degree first
                }
        Returns:
            The solution: sorted list of real roots (float), ascending order
        '''
        coeffs = problem.get("coefficients", [])
        if not coeffs or not isinstance(coeffs, list):
            return []
        # Remove leading zeros
        while coeffs and coeffs[0] == 0:
            coeffs = coeffs[1:]
        if not coeffs:
            return []
        degree = len(coeffs) - 1
        # Handle degree 0
        if degree == 0:
            return []
        # Degree 1: ax + b = 0
        if degree == 1:
            a, b = coeffs
            if a == 0:
                return []
            return [-b / a]
        # Degree 2: ax^2 + bx + c = 0
        if degree == 2:
            a, b, c = coeffs
            if a == 0:
                # Reduce to linear
                if b == 0:
                    return []
                return [-c / b]
            D = b*b - 4*a*c
            if D < 0:
                return []
            elif D == 0:
                return [-b / (2*a)]
            else:
                sqrtD = math.sqrt(D)
                r1 = (-b - sqrtD) / (2*a)
                r2 = (-b + sqrtD) / (2*a)
                return sorted([r1, r2])
        # Degree 3: cubic formula
        if degree == 3:
            a, b, c, d = coeffs
            if a == 0:
                # Reduce to quadratic
                return self.solve({"coefficients": [b, c, d]})
            # Depressed cubic: x^3 + px + q = 0
            p = (3*a*c - b*b) / (3*a*a)
            q = (2*b*b*b - 9*a*b*c + 27*a*a*d) / (27*a*a*a)
            # Discriminant
            D = (q/2)**2 + (p/3)**3
            roots = []
            if D > 0:
                # One real root
                sqrtD = math.sqrt(D)
                u = self._cubic_root(-q/2 + sqrtD)
                v = self._cubic_root(-q/2 - sqrtD)
                t = u + v
                root = t - b/(3*a)
                roots.append(root)
            elif D == 0:
                # Multiple real roots
                u = self._cubic_root(-q/2)
                t1 = 2*u - b/(3*a)
                t2 = -u - b/(3*a)
                roots.extend([t1, t2])
                if abs(u) < 1e-12:
                    roots.pop()  # Only one root
            else:
                # Three real roots
                r = math.sqrt(-(p/3)**3)
                phi = math.acos(-q/(2*r))
                m = 2 * math.sqrt(-p/3)
                t1 = m * math.cos(phi/3) - b/(3*a)
                t2 = m * math.cos((phi+2*math.pi)/3) - b/(3*a)
                t3 = m * math.cos((phi+4*math.pi)/3) - b/(3*a)
                roots.extend([t1, t2, t3])
            # Filter out small imaginary parts
            real_roots = []
            for r in roots:
                if isinstance(r, complex):
                    if abs(r.imag) < 1e-8:
                        real_roots.append(r.real)
                else:
                    real_roots.append(r)
            # Remove duplicates (for D=0)
            real_roots = list(set([round(x, 12) for x in real_roots]))
            return sorted(real_roots)
        # Degree 4: quartic formula (Ferrari's method)
        if degree == 4:
            a, b, c, d, e = coeffs
            if a == 0:
                return self.solve({"coefficients": [b, c, d, e]})
            # Depress quartic: x^4 + px^2 + qx + r = 0
            p = (8*a*c - 3*b*b) / (8*a*a)
            q = (b**3 - 4*a*b*c + 8*a*a*d) / (8*a*a*a)
            r = (-3*b**4 + 256*a**3*e - 64*a**2*b*d +
                 16*a*b*b*c - 16*a*a*c*c) / (256*a**4)
            # Ferrari's method
            roots = self._quartic_roots(a, b, c, d, e)
            # Filter real roots
            real_roots = []
            for r in roots:
                if isinstance(r, complex):
                    if abs(r.imag) < 1e-8:
                        real_roots.append(r.real)
                else:
                    real_roots.append(r)
            real_roots = list(set([round(x, 12) for x in real_roots]))
            return sorted(real_roots)
        # Degree > 4: use numpy.roots and filter real roots
        try:
            import numpy as np
            arr = np.array(coeffs, dtype=float)
            roots = np.roots(arr)
            real_roots = []
            for r in roots:
                if abs(r.imag) < 1e-8:
                    real_roots.append(r.real)
            real_roots = list(set([round(x, 12) for x in real_roots]))
            return sorted(real_roots)
        except ImportError:
            return []

    def is_solution(self, problem, solution):
        '''
        Check if the solution is correct for the given problem.
        Args:
            problem: Dictionary with "coefficients"
            solution: list of floats (roots)
        Returns:
            True if all roots are real roots of the polynomial (within tolerance), False otherwise
        '''
        coeffs = problem.get("coefficients", [])
        if not isinstance(solution, list):
            return False
        # Remove leading zeros
        while coeffs and coeffs[0] == 0:
            coeffs = coeffs[1:]
        if not coeffs:
            return solution == []
        # For each root, check if polynomial evaluates to zero (within tolerance)
        for x in solution:
            val = 0.0
            for i, a in enumerate(coeffs):
                val += a * (x ** (len(coeffs)-1-i))
            if abs(val) > 1e-6:
                return False
        # Check for duplicates in solution (roots should be unique)
        rounded = [round(x, 8) for x in solution]
        if len(set(rounded)) != len(rounded):
            return False
        return True

    def _cubic_root(self, x):
        if x >= 0:
            return x ** (1/3)
        else:
            return -(-x) ** (1/3)

    def _quartic_roots(self, a, b, c, d, e):
        # Ferrari's method for quartic equations
        # ax^4 + bx^3 + cx^2 + dx + e = 0
        # Returns list of roots (may be complex)
        if a == 0:
            # Reduce to cubic
            return self.solve({"coefficients": [b, c, d, e]})
        # Depress quartic: x = y - b/(4a)
        p = (8*a*c - 3*b*b) / (8*a*a)
        q = (b**3 - 4*a*b*c + 8*a*a*d) / (8*a*a*a)
        r = (-3*b**4 + 256*a**3*e - 64*a**2*b*d +
             16*a*b*b*c - 16*a*a*c*c) / (256*a**4)
        # Solve resolvent cubic: z^3 + 2pz^2 + (p^2 - 4r)z - q^2 = 0
        cubic_coeffs = [1, 2*p, p*p - 4*r, -q*q]
        z_roots = self.solve({"coefficients": cubic_coeffs})
        if not z_roots:
            return []
        z = max(z_roots)  # choose the largest real root
        if z < 0:
            u = 0
        else:
            u = math.sqrt(z)
        if abs(u) < 1e-12:
            v = w = 0
        else:
            v = math.sqrt(2*p + 2*z - q/u)
            w = math.sqrt(2*p + 2*z + q/u)
        shift = -b / (4*a)
        roots = []
        for sign1 in [1, -1]:
            for sign2 in [1, -1]:
                try:
                    if abs(u) < 1e-12:
                        root = shift + sign1 * v / 2
                    else:
                        root = shift + (sign1 * u + sign2 * v) / 2
                    roots.append(root)
                except Exception:
                    continue
        return roots
