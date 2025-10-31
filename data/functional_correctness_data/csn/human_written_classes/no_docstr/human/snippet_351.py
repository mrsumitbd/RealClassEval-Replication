from collections import defaultdict

class TokenIterator:

    def __init__(self, base_token):
        self.token = base_token
        self.counts = defaultdict(int)

    def __call__(self, est):
        typ = type(est)
        c = self.counts[typ]
        self.counts[typ] += 1
        return self.token if c == 0 else self.token + str(c)