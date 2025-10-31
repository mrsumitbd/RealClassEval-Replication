
class Factorization:
    @classmethod
    def factorize(cls, pq):
        """Return the prime factorization of an integer as a list of primes."""
        n = pq
        if n <= 1:
            return []

        factors = []
        # Handle factor 2 separately to allow step of 2 later
        while n % 2 == 0:
            factors.append(2)
            n //= 2

        # Check odd factors up to sqrt(n)
        i = 3
        max_factor = int(n**0.5) + 1
        while i <= max_factor and n > 1:
            while n % i == 0:
                factors.append(i)
                n //= i
                max_factor = int(n**0.5) + 1
            i += 2

        # If remaining n is a prime > 1
        if n > 1:
            factors.append(n)

        return factors

    @staticmethod
    def gcd(a, b):
        """Return the greatest common divisor of a and b using Euclid's algorithm."""
        while b:
            a, b = b, a % b
        return abs(a)
