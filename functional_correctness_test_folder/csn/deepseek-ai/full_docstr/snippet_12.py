
import random
import math


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

        y, c, m = random.randint(
            1, pq-1), random.randint(1, pq-1), random.randint(1, pq-1)
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for i in range(r):
                y = (pow(y, 2, pq) + c) % pq
            k = 0
            while k < r and g == 1:
                ys = y
                for i in range(min(m, r - k)):
                    y = (pow(y, 2, pq) + c) % pq
                    q = q * abs(x - y) % pq
                g = cls.gcd(q, pq)
                k += m
            r *= 2
        if g == pq:
            while True:
                ys = (pow(ys, 2, pq) + c) % pq
                g = cls.gcd(abs(x - ys), pq)
                if g > 1:
                    break
        return (g, pq // g) if g < pq // g else (pq // g, g)

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
        return a
