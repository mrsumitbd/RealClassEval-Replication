
class Factorization:
    '''
    Simple module to factorize large numbers really quickly.
    '''
    @classmethod
    def factorize(cls, pq):
        def pollard_rho(n):
            if n % 2 == 0:
                return 2
            x = 2
            y = 2
            d = 1
            def f(x): return (x * x + 1) % n
            while d == 1:
                x = f(x)
                y = f(f(y))
                d = cls.gcd(abs(x - y), n)
            if d == n:
                return None
            return d

        if not isinstance(pq, int) or pq < 1:
            raise ValueError("Input must be a positive integer.")

        factors = []
        n = pq
        while n > 1:
            factor = pollard_rho(n)
            if factor is None:
                factors.append(n)
                break
            factors.append(factor)
            n //= factor
        return factors

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
