
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
        if pq % 3 == 0:
            return (3, pq // 3)
        if pq % 5 == 0:
            return (5, pq // 5)

        # Pollard's Rho algorithm
        def f(x):
            return (x * x + 1) % pq

        x, y, d = 2, 2, 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = cls.gcd(abs(x - y), pq)

        if d == pq:
            return cls.factorize(pq)
        else:
            return (d, pq // d)

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
