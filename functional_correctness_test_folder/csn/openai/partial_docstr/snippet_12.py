
import random
import math
from typing import List


class Factorization:
    '''
    Simple module to factorize large numbers really quickly.
    '''
    @classmethod
    def factorize(cls, n: int) -> List[int]:
        """
        Return the prime factorization of n as a sorted list.
        """
        if n < 2:
            return []

        # Handle small primes quickly
        factors = []

        # Remove factors of 2
        while n % 2 == 0:
            factors.append(2)
            n //= 2

        if n == 1:
            return factors

        # If remaining n is prime, add it
        if cls._is_prime(n):
            factors.append(n)
            return sorted(factors)

        # Use Pollard's Rho to find a non-trivial factor
        factor = cls._pollard_rho(n)
        # Recursively factor the two parts
        factors += cls.factorize(factor)
        factors += cls.factorize(n // factor)

        return sorted(factors)

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Compute the greatest common divisor of a and b.
        """
        while b:
            a, b = b, a % b
        return a

    # ------------------------------------------------------------------
    # Internal helper methods
    # ------------------------------------------------------------------
    @staticmethod
    def _is_prime(n: int) -> bool:
        """
        Deterministic Miller–Rabin primality test for 64‑bit integers.
        """
        if n < 2:
            return False
        # Small primes
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for p in small_primes:
            if n % p == 0:
                return n == p

        # Write n-1 as d * 2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        # Deterministic bases for 64-bit integers
        bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
        for a in bases:
            if a % n == 0:
                continue
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def _pollard_rho(n: int) -> int:
        """
        Pollard's Rho algorithm to find a non‑trivial factor of n.
        """
        if n % 2 == 0:
            return 2
        # Random seed for reproducibility
        while True:
            c = random.randrange(1, n)
            def f(x): return (pow(x, 2, n) + c) % n
            x, y, d = 2, 2, 1
            while d == 1:
                x = f(x)
                y = f(f(y))
                d = Factorization.gcd(abs(x - y), n)
            if d != n:
                return d
