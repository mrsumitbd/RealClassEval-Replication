
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
        ''':returns: the lowest common ancestor of u and v
        :complexity: O(log n)
        '''
        if u == v:
            return u

        if self._level(u) < self._level(v):
            u, v = v, u

        diff = self._level(u) - self._level(v)
        u = self._move_up(u, diff)

        if u == v:
            return u

        for j in range(self.log_n - 1, -1, -1):
            if self.dp[u][j] != self.dp[v][j]:
                u = self.dp[u][j]
                v = self.dp[v][j]

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

    def _move_up(self, node, steps):
        for j in range(self.log_n):
            if steps & (1 << j):
                node = self.dp[node][j]
        return node
