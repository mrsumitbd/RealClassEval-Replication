
class Factorization:

    @classmethod
    def factorize(cls, pq):
        """Factorize a number that is a product of two prime numbers."""
        for i in range(2, int(pq ** 0.5) + 1):
            if pq % i == 0:
                return i, pq // i
        return 1, pq

    @staticmethod
    def gcd(a, b):
        """Compute the greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a
