
import math


class LowestCommonAncestorShortcuts:

    def __init__(self, prec):
        n = len(prec)
        if n == 0:
            return
        self.n = n
        self.L = math.floor(math.log2(n)) + 1 if n > 1 else 1
        self.up = [[-1] * n for _ in range(self.L)]

        for i in range(n):
            self.up[0][i] = prec[i]

        for k in range(1, self.L):
            for i in range(n):
                if self.up[k-1][i] != -1:
                    self.up[k][i] = self.up[k-1][self.up[k-1][i]]
                else:
                    self.up[k][i] = -1

    def query(self, u, v):
        if u == v:
            return u
        if self.up[self.L - 1][u] != self.up[self.L - 1][v]:
            return -1  # different trees

        # Bring u and v to the same level
        for k in range(self.L - 1, -1, -1):
            if self.up[k][u] != -1 and self.up[k][v] != -1 and self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]

        return self.up[0][u]
