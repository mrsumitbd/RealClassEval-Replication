
class LowestCommonAncestorShortcuts:

    def __init__(self, prec):
        n = len(prec)
        max_log = 0
        while (1 << max_log) < n:
            max_log += 1

        self.lift = [[-1] * max_log for _ in range(n)]

        for i in range(n):
            self.lift[i][0] = prec[i]

        for j in range(1, max_log):
            for i in range(n):
                if self.lift[i][j - 1] != -1:
                    self.lift[i][j] = self.lift[self.lift[i][j - 1]][j - 1]

    def query(self, u, v):
        if u == v:
            return u

        if u > v:
            u, v = v, u

        log = 0
        while (1 << (log + 1)) <= v:
            log += 1

        for j in range(log, -1, -1):
            if self.lift[v][j] >= u:
                v = self.lift[v][j]

        if u == v:
            return u

        for j in range(log, -1, -1):
            if self.lift[u][j] != self.lift[v][j]:
                u = self.lift[u][j]
                v = self.lift[v][j]

        return self.lift[u][0]
