import numpy as np
import itertools


class RectangleBin:
    '''
    An N-dimensional binary space partition tree for packing
    hyper-rectangles. Split logic is pure `numpy` but behaves
    similarly to `scipy.spatial.Rectangle`.
    Mostly useful for packing 2D textures and 3D boxes and
    has not been tested outside of 2 and 3 dimensions.
    Original article about using this for packing textures:
    http://www.blackpawn.com/texts/lightmaps/
    '''

    def __init__(self, bounds):
        '''
        Create a rectangular bin.
        Parameters
        ------------
        bounds : (2, dimension *) float
          Bounds array are `[mins, maxes]`
        '''
        b = np.asarray(bounds, dtype=float)
        if b.ndim != 2 or b.shape[0] != 2:
            raise ValueError("bounds must have shape (2, dim)")
        if not np.all(b[1] >= b[0]):
            raise ValueError("bounds must satisfy maxes >= mins")
        self.bounds = b.copy()
        self._children = None
        self._used = False

    @property
    def extents(self):
        return self.bounds[1] - self.bounds[0]

    def insert(self, size, rotate=True):
        size = np.asarray(size, dtype=float)
        if size.ndim != 1 or size.shape[0] != self.extents.shape[0]:
            raise ValueError(
                "size must be a 1D array with same dimension as bounds")
        if np.any(size < 0):
            return None

        eps = 1e-12

        def _fits(sz):
            return np.all(sz <= self.extents + eps)

        def _best_permutation():
            if not rotate:
                return np.arange(size.size), size
            best = None
            for perm in itertools.permutations(range(size.size)):
                perm = np.asarray(perm, dtype=int)
                szp = size[perm]
                if _fits(szp):
                    slack = self.extents - szp
                    # prefer tighter fits: minimize L-infinity, then L1, then lexicographic
                    key = (np.max(slack), np.sum(slack), tuple(slack))
                    if best is None or key < best[0]:
                        best = (key, perm, szp)
            return (best[1], best[2]) if best is not None else (None, None)

        # If this node is split, try children
        if self._children is not None:
            res = self._children[0].insert(size, rotate=rotate)
            if res is not None:
                return res
            return self._children[1].insert(size, rotate=rotate)

        # Leaf node
        if self._used:
            return None

        perm, sz = _best_permutation()
        if perm is None:
            return None

        slack = self.extents - sz
        if np.all(slack <= eps):
            self._used = True
            placed_mins = self.bounds[0].copy()
            placed_maxs = placed_mins + sz
            return np.stack([placed_mins, placed_maxs], axis=0)

        # Choose axis with largest slack to split
        axis = int(np.argmax(slack))
        split = self.bounds[0, axis] + sz[axis]

        # Create children
        b0 = self.bounds.copy()
        b1 = self.bounds.copy()
        b0[1, axis] = split
        b1[0, axis] = split

        left = RectangleBin(b0)
        right = RectangleBin(b1)
        self._children = (left, right)

        # Insert into left child; it will further split as needed
        return left.insert(sz, rotate=False)  # size already oriented
