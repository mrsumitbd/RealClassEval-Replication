class DiscretizedProcess:

    def iweight(self, i: int, j: int) -> float:
        raise Exception('Not Implemented.')

    def inode(self, i: int, j: int) -> float:
        raise Exception('Not Implemented.')

    def iteritems(self, i, eps=1e-16):
        for j in range(self.n_inodes(i)):
            w = self.iweight(i, j)
            if w > eps:
                x = self.inode(i, j)
                yield (w, x)