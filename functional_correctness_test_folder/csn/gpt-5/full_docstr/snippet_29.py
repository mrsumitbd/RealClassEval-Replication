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

    class _Node:
        __slots__ = ("mins", "maxs", "left", "right", "used")

        def __init__(self, mins, maxs):
            self.mins = mins
            self.maxs = maxs
            self.left = None
            self.right = None
            self.used = False

        @property
        def extents(self):
            return self.maxs - self.mins

        def is_leaf(self):
            return self.left is None and self.right is None

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
            raise ValueError("bounds must be shape (2, dimension)")
        mins = b[0].astype(float)
        maxs = b[1].astype(float)
        if mins.shape != maxs.shape:
            raise ValueError("mins and maxs must have the same shape")
        if np.any(maxs < mins):
            raise ValueError("All maxs must be >= mins")
        self._dim = mins.size
        self._root = RectangleBin._Node(mins.copy(), maxs.copy())

    @property
    def extents(self):
        '''
        Bounding box size.
        Returns
        ----------
        extents : (dimension,) float
          Edge lengths of bounding box
        '''
        return self._root.extents.copy()

    def _insert_node(self, node, size):
        # If this node has been split, try children
        if not node.is_leaf():
            pos = self._insert_node(node.left, size)
            if pos is not None:
                return pos
            return self._insert_node(node.right, size)

        # If already used, cannot place here
        if node.used:
            return None

        space = node.extents
        leftover = space - size

        # If it doesn't fit, bail
        if np.any(leftover < 0):
            return None

        # Perfect fit: occupy node
        if np.allclose(leftover, 0):
            node.used = True
            return node.mins.copy()

        # Split along axis with the most leftover space
        axis = int(np.argmax(leftover))
        cut = node.mins[axis] + size[axis]

        # Left child: from mins to cut along axis
        left_mins = node.mins.copy()
        left_maxs = node.maxs.copy()
        left_maxs[axis] = cut

        # Right child: from cut to maxs along axis
        right_mins = node.mins.copy()
        right_mins[axis] = cut
        right_maxs = node.maxs.copy()

        node.left = RectangleBin._Node(left_mins, left_maxs)
        node.right = RectangleBin._Node(right_mins, right_maxs)

        # Try to insert into the left child (tight fit region)
        return self._insert_node(node.left, size)

    def insert(self, size, rotate=True):
        '''
        Insert a rectangle into the bin.
        Parameters
        -------------
        size : (dimension,) float
          Size of rectangle to insert/
        Returns
        ----------
        inserted : (2,) float or None
          Position of insertion in the tree or None
          if the insertion was unsuccessful.
        '''
        sz = np.asarray(size, dtype=float).reshape(-1)
        if sz.size != self._dim:
            raise ValueError(f"size must be of length {self._dim}")

        # Generate size permutations for rotation if allowed
        if rotate and self._dim > 1:
            perms = list(dict.fromkeys(
                itertools.permutations(range(self._dim))))
        else:
            perms = [tuple(range(self._dim))]

        # Try each permutation until one fits
        for perm in perms:
            permuted_size = sz[list(perm)]
            pos = self._insert_node(self._root, permuted_size)
            if pos is not None:
                return pos

        return None
