
class LowestCommonAncestorShortcuts:
    '''Lowest common ancestor data structure using shortcuts to ancestors
    '''

    def __init__(self, prec):
        '''builds the structure from a given tree
        :param prec: father for every node, with prec[0] = 0
        :assumes: prec[node] < node
        :complexity: O(n log n), with n = len(nodes)
        '''
        self.n = len(prec)
        self.log_n = self._get_log_n()
        self.dp = [[-1] * self.log_n for _ in range(self.n)]

        for i in range(self.n):
            self.dp[i][0] = prec[i]

        for j in range(1, self.log_n):
            for i in range(self.n):
                if self.dp[i][j - 1] != -1:
                    self.dp[i][j] = self.dp[self.dp[i][j - 1]][j - 1]

    def query(self, u, v):
        if u == v:
            return u

        if self._level(u) < self._level(v):
            u, v = v, u

        diff = self._level(u) - self._level(v)
        k = 0
        while diff:
            if diff & 1:
                u = self.dp[u][k]
            diff >>= 1
            k += 1

        if u == v:
            return u

        for k in range(self.log_n - 1, -1, -1):
            if self.dp[u][k] != -1 and self.dp[u][k] != self.dp[v][k]:
                u = self.dp[u][k]
                v = self.dp[v][k]

        return self.dp[u][0]

    def _get_log_n(self):
        log_n = 0
        while (1 << log_n) < self.n:
            log_n += 1
        return log_n

    def _level(self, node):
        level = 0
        while node != 0:
            node = self.dp[node][0]
            level += 1
        return level
