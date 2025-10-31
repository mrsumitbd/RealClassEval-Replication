from collections import Counter, defaultdict

class umi:

    def __init__(self, seq):
        self.seq = defaultdict(list)
        self.times = 0
        self.update(seq)

    def update(self, seq, counts=1):
        for pos, nt in enumerate(seq):
            self.seq[pos].append(nt)
        self.times += counts

    def get(self):
        seq = ''
        for pos in sorted(self.seq.keys()):
            lst = self.seq[pos]
            seq += max(lst, key=lst.count)
        return seq