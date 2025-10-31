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
        n = int(pq)
        if n <= 1:
            return (n, 1)
        if n % 2 == 0:
            return (2, n // 2)

        import random

        def brent(N):
            if N % 2 == 0:
                return 2
            if N % 3 == 0:
                return 3
            # Random parameters for the polynomial x^2 + c
            y = random.randrange(1, N)
            c = random.randrange(1, N)
            m = random.randrange(1, N)
            g = 1
            r = 1
            q = 1
            while g == 1:
                x = y
                for _ in range(r):
                    y = (y * y + c) % N
                k = 0
                while k < r and g == 1:
                    ys = y
                    for _ in range(min(m, r - k)):
                        y = (y * y + c) % N
                        q = (q * abs(x - y)) % N
                    g = cls.gcd(q, N)
                    k += m
                r <<= 1
            if g == N:
                while True:
                    ys = (ys * ys + c) % N
                    g = cls.gcd(abs(x - ys), N)
                    if g > 1:
                        break
            return g

        # Keep trying until a non-trivial factor is found
        while True:
            g = brent(n)
            if 1 < g < n:
                p = g
                q = n // g
                return (p, q)

    @staticmethod
    def gcd(a, b):
        '''
        Calculates the Greatest Common Divisor.
        :param a: the first number.
        :param b: the second number.
        :return: GCD(a, b)
        '''
        a = abs(int(a))
        b = abs(int(b))
        while b:
            a, b = b, a % b
        return a
