
class Factorization:

    @classmethod
    def factorize(cls, pq):

        if pq % 2 == 0:
            return (2, pq // 2)
        i = 3
        max_factor = int(pq**0.5) + 1
        while i <= max_factor:
            if pq % i == 0:
                return (i, pq // i)
            i += 2
        return (pq, 1)

    @staticmethod
    def gcd(a, b):

        while b:
            a, b = b, a % b
        return a
