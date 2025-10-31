class intlabel_disjointsets:
    """A disjoint sets implementation with size and path-halving, for graphs 
    labeled [0, ..., n-1]

    Args:
        n (int):
            The number of items in the disjoint sets

    """

    def __init__(self, n):
        self._parent = list(range(n))
        self._size = [1] * n

    def find(self, q):
        """Find the current root for q.

        Args:
            q (int):
                A number in range(n)

        Returns:
            int: the root of the set containing q

        """
        parent = self._parent
        p = parent[q]
        while q != p:
            r = parent[q] = parent[p]
            q, p = (p, r)
        return p

    def union(self, p, q):
        """Merges the sets containing p and q.

        Args:
            p (int):
                A number in range(n)
            q (int):
                A number in range(n)

        """
        p = self.find(p)
        q = self.find(q)
        a = self._size[p]
        b = self._size[q]
        if p == q:
            return
        if a > b:
            p, q = (q, p)
        self._parent[p] = q
        self._size[q] = a + b

    def size(self, q):
        """Returns the size of the set containing q.

        Args:
            p (int):
                A number in range(n)

        Returns:
            int: the size of the set containing q
        """
        return self._size[self.find(q)]