
class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        pass

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        coefficients = problem.get('coefficients', [])
        roots = []
        if len(coefficients) == 0:
            return roots
        if len(coefficients) == 1:
            if coefficients[0] == 0:
                return ["Infinite solutions"]
            else:
                return roots
        if len(coefficients) == 2:
            a, b = coefficients
            if a == 0:
                if b == 0:
                    return ["Infinite solutions"]
                else:
                    return roots
            root = -b / a
            roots.append(root)
            return roots
        if len(coefficients) == 3:
            a, b, c = coefficients
            discriminant = b**2 - 4 * a * c
            if discriminant > 0:
                root1 = (-b + discriminant**0.5) / (2 * a)
                root2 = (-b - discriminant**0.5) / (2 * a)
                roots.extend([root1, root2])
            elif discriminant == 0:
                root = -b / (2 * a)
                roots.append(root)
            return roots
        return roots

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if solution == ["Infinite solutions"]:
            return all(coef == 0 for coef in problem.get('coefficients', []))
        coefficients = problem.get('coefficients', [])
        if not coefficients:
            return solution == []
        for root in solution:
            value = 0
            for i, coef in enumerate(coefficients):
                value += coef * (root ** (len(coefficients) - i - 1))
            if not abs(value) < 1e-6:
                return False
        return True
