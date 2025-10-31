
class PolynomialReal:

    def __init__(self):
        # Initialize an empty list to store coefficients
        self.coefficients = []

    def solve(self, problem):
        """
        Solve a polynomial equation of the form ax^n + bx^(n-1) + ... + cx + d = 0.

        Args:
        problem (list): A list of coefficients in descending order of powers.

        Returns:
        list: A list of real roots of the polynomial equation.
        """
        import numpy as np

        # Store the coefficients
        self.coefficients = problem

        # Use numpy to find the roots
        roots = np.roots(self.coefficients)

        # Filter out complex roots and return real roots
        real_roots = [root.real for root in roots if np.isreal(root)]

        return real_roots

    def is_solution(self, problem, solution):
        """
        Check if a given solution satisfies a polynomial equation.

        Args:
        problem (list): A list of coefficients in descending order of powers.
        solution (float): A potential solution to the polynomial equation.

        Returns:
        bool: True if the solution satisfies the equation, False otherwise.
        """
        # Evaluate the polynomial at the given solution
        result = sum([coeff * (solution ** (len(problem) - 1 - i))
                     for i, coeff in enumerate(problem)])

        # Check if the result is close to zero (due to floating point precision)
        return abs(result) < 1e-6


# Example usage:
if __name__ == "__main__":
    poly = PolynomialReal()
    problem = [1, -6, 11, -6]  # represents x^3 - 6x^2 + 11x - 6 = 0
    solutions = poly.solve(problem)
    print("Solutions:", solutions)

    for solution in solutions:
        print(f"Is {solution} a solution?",
              poly.is_solution(problem, solution))
