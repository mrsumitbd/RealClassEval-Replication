
class Factorization:
    '''
    Simple module to factorize large numbers really quickly.
    '''
    @classmethod
    def factorize(cls, pq):
        if pq < 2:
            return []
        # Use trial division up to 10^6, then Pollard's Rho

        def _factor(n):
            factors = []
            # Trial division for small primes
            for p in [2, 3, 5]:
                while n % p == 0:
                    factors.append(p)
                    n //= p
            i = 7
            w = 4
            while i * i <= n and i < 10**6:
                while n % i == 0:
                    factors.append(i)
                    n //= i
                i += w
                w = 6 - w
            if n == 1:
                return factors
            # Use Pollard's Rho for remaining composite

            def pollards_rho(n):
                if n % 2 == 0:
                    return 2
                if n % 3 == 0:
                    return 3
                if n % 5 == 0:
                    return 5
                import random
                while True:
                    c = random.randrange(1, n)
                    def f(x): return (pow(x, 2, n) + c) % n
                    x, y, d = 2, 2, 1
                    while d == 1:
                        x = f(x)
                        y = f(f(y))
                        d = cls.gcd(abs(x - y), n)
                    if d != n:
                        return d
            # If n is prime

            def is_prime(n):
                if n < 2:
                    return False
                if n == 2 or n == 3:
                    return True
                if n % 2 == 0 or n % 3 == 0:
                    return False
                i = 5
                w = 2
                while i * i <= n:
                    if n % i == 0:
                        return False
                    i += w
                    w = 6 - w
                return True
            stack = [n]
            while stack:
                m = stack.pop()
                if m == 1:
                    continue
                if is_prime(m):
                    factors.append(m)
                    continue
                d = pollards_rho(m)
                stack.append(d)
                stack.append(m // d)
            return sorted(factors)
        return _factor(pq)

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)
