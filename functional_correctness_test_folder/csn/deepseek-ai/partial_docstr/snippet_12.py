
import math
import random


class Factorization:
    '''
    Simple module to factorize large numbers really quickly.
    '''
    @classmethod
    def factorize(cls, pq):
        if pq % 2 == 0:
            return (2, pq // 2)

        def pollards_rho(n):
            if n % 2 == 0:
                return 2
            if n % 3 == 0:
                return 3
            if n % 5 == 0:
                return 5

            while True:
                c = random.randint(1, n-1)
                def f(x): return (pow(x, 2, n) + c) % n
                x, y, d = 2, 2, 1
                while d == 1:
                    x = f(x)
                    y = f(f(y))
                    d = math.gcd(abs(x - y), n)
                if d != n:
                    return d

        def _factor(n):
            if n == 1:
                return []
            if cls.is_prime(n):
                return [n]
            d = pollards_rho(n)
            return _factor(d) + _factor(n // d)

        factors = _factor(pq)
        return (factors[0], pq // factors[0])

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def is_prime(n, k=5):
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0:
            return False

        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for __ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
