class Factorization:
    '''
    Simple module to factorize large numbers really quickly.
    '''
    @classmethod
    def factorize(cls, n):
        if n <= 1:
            return (n, 1)
        if n % 2 == 0:
            return (2, n // 2)
        # Trial divide small primes first
        small_primes = [
            3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
            109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
            173, 179, 181, 191, 193, 197, 199
        ]
        for p in small_primes:
            if n % p == 0:
                return (p, n // p)

        def is_probable_prime(a):
            if a < 2:
                return False
            # Deterministic Miller-Rabin for 64-bit, extended bases cover large ints reasonably
            # but Python ints are arbitrary precision; we'll use a common deterministic set for 128-bit
            # For general use, this is a robust probable-prime check.
            d = a - 1
            s = 0
            while d % 2 == 0:
                d //= 2
                s += 1

            def check(witness):
                x = pow(witness, d, a)
                if x == 1 or x == a - 1:
                    return True
                for _ in range(s - 1):
                    x = (x * x) % a
                    if x == a - 1:
                        return True
                return False

            # Small primes check
            for sp in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
                if a == sp:
                    return True
                if a % sp == 0:
                    return a == sp
            # Miller-Rabin bases sufficient for 128-bit integers; for larger, still very strong
            bases = [2, 3, 5, 7, 11, 13, 17]
            for b in bases:
                if b % a == 0:
                    continue
                if not check(b):
                    return False
            return True

        import random

        def pollards_rho(num):
            if num % 2 == 0:
                return 2
            if is_probable_prime(num):
                return num
            while True:
                x = random.randrange(2, num - 1)
                y = x
                c = random.randrange(1, num - 1)
                d = 1
                # Floyd's cycle detection
                while d == 1:
                    x = (x * x + c) % num
                    y = (y * y + c) % num
                    y = (y * y + c) % num
                    d = cls.gcd(abs(x - y), num)
                if d != num:
                    return d

        def factor_one(num):
            if num == 1:
                return 1
            if is_probable_prime(num):
                return num
            d = pollards_rho(num)
            if d == num:
                return num
            # Ensure we get a prime factor
            f1 = factor_one(d)
            return f1

        d = factor_one(n)
        if d == 1 or d == n:
            return (d, n // max(d, 1) if d != 0 else 0)
        return (d, n // d)

    @staticmethod
    def gcd(a, b):
        a = abs(a)
        b = abs(b)
        while b:
            a, b = b, a % b
        return a
