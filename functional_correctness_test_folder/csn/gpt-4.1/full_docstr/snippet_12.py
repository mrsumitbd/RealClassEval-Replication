
import random


class Factorization:
    '''
    Simple module to factorize large numbers really quickly.
    '''
    @classmethod
    def factorize(cls, pq):
        '''
        Factorizes the given large integer.
        Implementation from https://comeoncodeon.wordpress.com/2010/09/18/pollard-rho-brent-integer-factorization/.
        :param pq: the prime pair pq.
        :return: a tuple containing the two factors p and q.
        '''
        if pq % 2 == 0:
            return (2, pq // 2)
        if pq < 4:
            return (1, pq)

        def brent(N):
            if N % 2 == 0:
                return 2
            y, c, m = random.randrange(1, N), random.randrange(
                1, N), random.randrange(1, N)
            g, r, q = 1, 1, 1
            while g == 1:
                x = y
                for i in range(r):
                    y = (pow(y, 2, N) + c) % N
                k = 0
                while k < r and g == 1:
                    ys = y
                    for i in range(min(m, r - k)):
                        y = (pow(y, 2, N) + c) % N
                        q = q * abs(x - y) % N
                    g = cls.gcd(q, N)
                    k += m
                r *= 2
            if g == N:
                while True:
                    ys = (pow(ys, 2, N) + c) % N
                    g = cls.gcd(abs(x - ys), N)
                    if g > 1:
                        break
            return g
        factor = brent(pq)
        if factor == pq or factor == 1:
            return (1, pq)
        return (factor, pq // factor)

    @staticmethod
    def gcd(a, b):
        '''
        Calculates the Greatest Common Divisor.
        :param a: the first number.
        :param b: the second number.
        :return: GCD(a, b)
        '''
        while b:
            a, b = b, a % b
        return abs(a)
