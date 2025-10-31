
class Factorization:

    @classmethod
    def factorize(cls, pq):
        a = 0
        b = 0
        while a * a <= pq:
            a += 1
            b_squared = a * a - pq
            b = int(b_squared**0.5)
            if b * b == b_squared:
                return a, b
        return None, None

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
