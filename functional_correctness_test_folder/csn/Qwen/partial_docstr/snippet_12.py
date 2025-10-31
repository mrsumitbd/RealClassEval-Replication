
class Factorization:
    '''
    Simple module to factorize large numbers really quickly.
    '''
    @classmethod
    def factorize(cls, pq):
        a = 0
        while True:
            a += 1
            x = a * a - pq
            y = int(x**0.5)
            if y * y == x:
                p = a - y
                q = a + y
                return p, q

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
