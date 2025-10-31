
class ChandrasekharSieve:
    """
    This is a class that uses the Chandrasekhar's Sieve method to find all prime numbers within the range
    """

    def __init__(self, n):
        """
        Initialize the ChandrasekharSieve class with the given limit.
        :param n: int, the upper limit for generating prime numbers
        """
        self.n = n
        self.primes = self.generate_primes()

    def generate_primes(self):
        """
        Generate prime numbers up to the specified limit using the Chandrasekhar sieve algorithm.
        :return: list, a list of prime numbers
        >>> cs = ChandrasekharSieve(20)
        >>> cs.generate_primes()
        [2, 3, 5, 7, 11, 13, 17, 19]
        """
        if self.n < 2:
            return []

        # Boolean array where index represents the number.
        # True means "potentially prime".
        is_prime = [True] * (self.n + 1)
        is_prime[0:2] = [False, False]  # 0 and 1 are not prime

        # Chandrasekhar's sieve: iterate over odd numbers only after handling 2
        for p in range(2, int(self.n ** 0.5) + 1):
            if is_prime[p]:
                # Mark multiples of p as non-prime
                step = p
                start = p * p
                is_prime[start:self.n + 1:step] = [False] * \
                    len(is_prime[start:self.n + 1:step])

        # Extract primes
        return [i for i, prime in enumerate(is_prime) if prime]

    def get_primes(self):
        """
        Get the list of generated prime numbers.
        :return: list, a list of prime numbers
        >>> cs = ChandrasekharSieve(20)
        >>> cs.get_primes()
        [2, 3, 5, 7, 11, 13, 17, 19]
        """
        return self.primes
