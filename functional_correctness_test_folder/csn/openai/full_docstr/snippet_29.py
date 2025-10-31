
import numpy as np


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
            self.bounds = bounds  # (2, dim) array
            self.used = False
            self.children = None  # [left, right]

    def __init__(self, bounds):
        '''
        Create a rectangular bin.
        Parameters
        ------------
        bounds : (2, dimension *) float
          Bounds array are `[mins, maxes]`
        '''
        self.bounds = np.asarray(bounds, dtype=float)
        if self.bounds.shape != (2, self.bounds.shape[1]):
            raise ValueError("bounds must be shape (2, dim)")
        self.root = self._Node(self.bounds)

    @property
    def extents(self):
        '''
        Bounding box size.
        Returns
        ----------
        extents : (dimension,) float
          Edge lengths of bounding box
        '''
        return self.bounds[1] - self.bounds[0]

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
        size = np.asarray(size, dtype=float)
        if size.ndim != 1:
            raise ValueError("size must be 1-D array")
        if size.shape[0] != self.bounds.shape[1]:
            raise ValueError("size dimension must match bin dimension")

        # Try original orientation
        pos = self._insert(self.root, size)
        if pos is not None:
            return pos

        # Try rotated orientation if allowed
        if rotate and size.shape[0] == 2:
            rotated = size[::-1]
            pos = self._insert(self.root, rotated)
            if pos is not None:
                return pos

        return None

    def _insert(self, node, size):
        # If node has children, try them
        if node.children is not None:
            for child in node.children:
                pos = self._insert(child, size)
                if pos is not None:
                    return pos
            return None

        # If node is already used, cannot insert
        if node.used:
            return None

        # Check if rectangle fits in this node
        node_extents = node.bounds[1] - node.bounds[0]
        if np.any(size > node_extents):
            return None

        # If rectangle exactly matches node, occupy it
        if np.allclose(size, node_extents):
            node.used = True
            return node.bounds[0].copy()

        # Otherwise split node
        diff = node_extents - size
        # Choose split direction: larger leftover dimension
        split_dim = np.argmax(diff)
        # Determine split position
        split_pos = node.bounds[0][split_dim] + size[split_dim]

        # Create children bounds
        left_bounds = node.bounds.copy()
        right_bounds = node.bounds.copy()

        # Left child will contain the rectangle
        left_bounds[1][split_dim] = split_pos
        # Right child will contain the remaining space
        right_bounds[0][split_dim] = split_pos

        node.children = [self._Node(left_bounds), self._Node(right_bounds)]
        node.used = False  # internal node

        # Try inserting into left child first
        return self._insert(node.children[0], size)
