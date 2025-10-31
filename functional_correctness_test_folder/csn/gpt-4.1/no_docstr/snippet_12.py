
class Factorization:

    @classmethod
    def factorize(cls, pq):
        for i in range(2, int(pq ** 0.5) + 1):
            if pq % i == 0:
                return (i, pq // i)
        return (pq, 1)

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
