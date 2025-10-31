
import numpy as np
from itertools import permutations


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
        __slots__ = ("bounds", "used", "children")

        def __init__(self, bounds):
            self.bounds = bounds          # (2, dim) array
            self.used = False
            self.children = None          # None or [left, right]

        def _fits(self, size):
            """Return True if size fits in this node."""
            mins, maxs = self.bounds
            return np.all(size <= (maxs - mins))

        def _split(self, size):
            """Split this node into two children along the axis with
            the largest leftover space."""
            mins, maxs = self.bounds
            dims = maxs - mins
            leftover = dims - size
            # choose axis with largest leftover > 0
            axis = np.argmax(leftover)
            # create child1: the rectangle region
            child1_bounds = np
