
class LowestCommonAncestorShortcuts:

    def __init__(self, prec):
        self.n = len(prec)
        self.logn = 0
        while (1 << self.logn) < self.n:
            self.logn += 1
        self.prec = prec
        self.shortcuts = [[-1] * self.n for _ in range(self.logn)]
        for i in range(self.n):
            self.shortcuts[0][i] = prec[i]
        for j in range(1, self.logn):
            for i in range(self.n):
                if self.shortcuts[j-1][i] != -1:
                    self.shortcuts[j][i] = self.shortcuts[j -
                                                          1][self.shortcuts[j-1][i]]

    def query(self, u, v):
        if u == v:
            return u
        if u > v:
            u, v = v, u
        log = 0
        while (1 << log) <= v - u:
            log += 1
        log -= 1
        for i in range(log, -1, -1):
            if v - (1 << i) >= u:
                v = self.shortcuts[i][v]
        if u == v:
            return u
        for i in range(log, -1, -1):
            if self.shortcuts[i][u] != -1 and self.shortcuts[i][u] != self.shortcuts[i][v]:
                u = self.shortcuts[i][u]
                v = self.shortcuts[i][v]
        return self.prec[u]
