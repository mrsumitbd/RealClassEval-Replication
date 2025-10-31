class Factorization:

    @classmethod
    def factorize(cls, pq):
        n = abs(int(pq))
        if n < 2:
            return (n, 1)
        if n % 2 == 0:
            return (2, n // 2)
        i = 3
        while i * i <= n:
            if n % i == 0:
                return (i, n // i)
            i += 2
        return (n, 1)

    @staticmethod
    def gcd(a, b):
        a, b = abs(int(a)), abs(int(b))
        while b:
            a, b = b, a % b
        return a
