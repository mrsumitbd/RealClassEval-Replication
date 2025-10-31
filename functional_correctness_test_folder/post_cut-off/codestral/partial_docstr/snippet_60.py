
class PolynomialReal:

    def __init__(self):

        pass

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        coefficients = problem['coefficients']
        degree = len(coefficients) - 1
        roots = []

        if degree == 1:
            roots.append(-coefficients[1] / coefficients[0])
        elif degree == 2:
            a, b, c = coefficients
            discriminant = b**2 - 4*a*c
            if discriminant >= 0:
                roots.append((-b + discriminant**0.5) / (2*a))
                roots.append((-b - discriminant**0.5) / (2*a))
        elif degree == 3:
            a, b, c, d = coefficients
            p = (3*a*c - b**2) / (3*a**2)
            q = (2*b**3 - 9*a*b*c + 27*a**2*d) / (27*a**3)
            discriminant = (q/2)**2 + (p/3)**3

            if discriminant > 0:
                u = (-q/2 + discriminant**0.5)**(1/3)
                v = (-q/2 - discriminant**0.5)**(1/3)
                roots.append(u + v - b/(3*a))
            elif discriminant == 0:
                if p == q == 0:
                    roots.append(-b/(3*a))
                else:
                    roots.append(3*q/p - b/(3*a))
                    roots.append(-3*q/(2*p) - b/(3*a))
            else:
                import cmath
                omega = cmath.exp(2j * cmath.pi / 3)
                for k in range(3):
                    roots.append(2 * (-p/3)**0.5 * cmath.cos((cmath.acos(3 *
                                 q/(2*p) * (-3/p)**0.5) + 2*k*cmath.pi)/3) - b/(3*a))

        return {'roots': roots}

    def is_solution(self, problem, solution):

        coefficients = problem['coefficients']
        roots = solution['roots']
        tolerance = 1e-6

        for root in roots:
            value = sum(coeff * (root ** i)
                        for i, coeff in enumerate(coefficients))
            if abs(value) > tolerance:
                return False

        return True
