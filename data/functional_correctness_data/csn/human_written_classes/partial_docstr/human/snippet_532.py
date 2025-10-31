import numpy as np
from numpy import random

class MultinomialQueue:
    """On-the-fly generator for the multinomial distribution.

    To obtain k1,k2, ... draws from the multinomial distribution with
    weights W, do::

        g = MulinomialQueue(M,W)
        first_set_of_draws = g.dequeue(k1)
        second_set_of_draws = g.dequeue(k2)
        #\xa0... and so on

    At initialisation, a vector of size M is created, and each time dequeue(k)
    is invoked, the next k draws are produced. When all the draws have been
    "served", a new vector of size M is generated. (If no value is given
    for M, we take M=N, the length of vector W.)

    In this way, we have on average a O(1) complexity for each draw,
    without knowing in advance how many draws will be needed.
    """

    def __init__(self, W, M=None):
        self.W = W
        self.M = W.size if M is None else M
        self.j = 0
        self.enqueue()

    def enqueue(self):
        perm = random.permutation(self.M)
        self.A = multinomial(self.W, M=self.M)[perm]

    def dequeue(self, k):
        """Outputs *k* draws from the multinomial distribution."""
        if self.j + k <= self.M:
            out = self.A[self.j:self.j + k]
            self.j += k
        elif k <= self.M:
            out = np.empty(k, dtype=np.int64)
            nextra = self.j + k - self.M
            out[:k - nextra] = self.A[self.j:]
            self.enqueue()
            out[k - nextra:] = self.A[:nextra]
            self.j = nextra
        else:
            raise ValueError('MultinomialQueue: k must be <= M (the max                              capacity of the queue)')
        return out