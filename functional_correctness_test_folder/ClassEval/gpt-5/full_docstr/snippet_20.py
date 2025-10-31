class ChandrasekharSieve:
    """
    This is a class that uses the Chandrasekhar's Sieve method to find all prime numbers within the range
    """

    def __init__(self, n):
        """
        Initialize the ChandrasekharSieve class with the given limit.
        :param n: int, the upper limit for generating prime numbers
        """
        self.n = int(n)
        self.primes = self.generate_primes()

    def generate_primes(self):
        """
        Generate prime numbers up to the specified limit using the Chandrasekhar sieve algorithm.
        :return: list, a list of prime numbers
        >>> cs = ChandrasekharSieve(20)
        >>> cs.generate_primes()
        [2, 3, 5, 7, 11, 13, 17, 19]

        """
        n = self.n
        if n < 2:
            return []
        # Sieve of Sundaram (often misattributed; here referred to as Chandrasekhar's sieve)
        m = (n - 1) // 2
        marked = [False] * (m + 1)
        i = 1
        while i <= m:
            j = i
            while i + j + 2 * i * j <= m:
                marked[i + j + 2 * i * j] = True
                j += 1
            i += 1

        primes = [2] if n >= 2 else []
        primes.extend(2 * k + 1 for k in range(1, m + 1)
                      if not marked[k] and 2 * k + 1 <= n)
        return primes

    def get_primes(self):
        """
        Get the list of generated prime numbers.
        :return: list, a list of prime numbers
        >>> cs = ChandrasekharSieve(20)
        >>> cs.get_primes()
        [2, 3, 5, 7, 11, 13, 17, 19]

        """
        return self.primes
