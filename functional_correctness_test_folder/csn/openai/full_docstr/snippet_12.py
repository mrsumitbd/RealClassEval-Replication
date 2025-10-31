
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
        n = pq
        if n <= 1:
            return (n, 1)
        # trivial small factor
        if n % 2 == 0:
            return (2, n // 2)

        # Brent's algorithm
        def pollard_rho_brent(n):
            if n % 2 == 0:
                return 2
            # random seed
            y = random.randrange(1, n)
            c = random.randrange(1, n)
            m = random.randrange(1, n)
            g = 1
            r = 1
            q = 1
            while g == 1:
                x = y
                for _ in range(r):
                    y = (pow(y, 2, n) + c) % n
                k = 0
                while k < r and g == 1:
                    ys = y
                    for _ in range(min(m, r - k)):
                        y = (pow(y, 2, n) + c) % n
                        q = (q * abs(x - y)) % n
                    g = cls.gcd(q, n)
                    k += m
                r <<= 1
            if g == n:
                while True:
                    ys = (pow(ys, 2, n) + c) % n
                    g = cls.gcd(abs(x - ys), n)
                    if g > 1:
                        break
            return g

        factor = pollard_rho_brent(n)
        if factor == n:
            # n is probably prime
            return (n, 1)
        return (factor, n // factor)

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
