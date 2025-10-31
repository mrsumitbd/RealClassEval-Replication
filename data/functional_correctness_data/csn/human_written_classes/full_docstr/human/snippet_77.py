from bisect import bisect_left
import random

class Permute:
    """
    Permute provide a random [n] -> [n] permute operation.
    e.g, a [3] -> [3] permute operation could be:
    [0,1,2] -> [1,0,2], "010" => "100"
    """

    def __init__(self, n):
        """
        Init a Permute object. Randomly generate a mapping, e.g. [0,1,2] -> [1,0,2]
        """
        m = list(range(n))
        for end in xrange(n - 1, 0, -1):
            r = random.randint(0, end)
            tmp = m[end]
            m[end] = m[r]
            m[r] = tmp
        self.mapping = m

    def permute(self, ba):
        """
        Permute the bitarray ba inplace.
        """
        c = ba.copy()
        for i in xrange(len(self.mapping)):
            ba[i] = c[self.mapping[i]]
        return ba

    def revert(self, ba):
        """
        Reversely permute the bitarray ba inplace.
        """
        c = ba.copy()
        for i in xrange(len(self.mapping)):
            ba[self.mapping[i]] = c[i]
        return ba

    def search_revert(self, bas, ba, beam_size):
        """
        ba: query bitarray
        bas: a sorted list of tuples of (permuted bitarray, original bitarray)
        return : query bitarray's beam-size neighbours (unpermuted bitarray)
        """
        pba = ba.copy()
        self.permute(pba)
        assert beam_size % 2 == 0
        half_beam = beam_size / 2
        idx = bisect_left(bas, (pba, ba))
        start = int(max(0, idx - half_beam))
        end = int(min(len(bas), idx + half_beam))
        res = bas[start:end]
        res = [x[1] for x in res]
        return res