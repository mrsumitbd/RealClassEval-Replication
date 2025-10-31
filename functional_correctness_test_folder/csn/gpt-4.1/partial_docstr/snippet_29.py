
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

    def __init__(self, bounds):
        '''
        Create a rectangular bin.
        Parameters
        ------------
        bounds : (2, dimension *) float
          Bounds array are `[mins, maxes]`
        '''
        self.bounds = np.array(bounds, dtype=float)
        self.dimension = self.bounds.shape[1]
        self.left = None
        self.right = None
        self.occupied = False

    @property
    def extents(self):
        return self.bounds.copy()

    def insert(self, size, rotate=True):
        size = np.array(size, dtype=float)
        # If this node has children, try to insert into them
        if self.left is not None and self.right is not None:
            result = self.left.insert(size, rotate)
            if result is not None:
                return result
            return self.right.insert(size, rotate)

        # If already occupied, can't insert here
        if self.occupied:
            return None

        # Try all rotations if allowed
        size_options = [size]
        if rotate:
            from itertools import permutations
            perms = set(tuple(x) for x in permutations(size))
            size_options = [np.array(x) for x in perms]

        for sz in size_options:
            min_corner = self.bounds[0]
            max_corner = self.bounds[1]
            available = max_corner - min_corner
            fits = np.all(sz <= available + 1e-8)
            if not fits:
                continue

            # If fits exactly, occupy this node
            if np.allclose(sz, available):
                self.occupied = True
                return np.stack([min_corner, min_corner + sz])

            # Otherwise, split
            # Find first axis where we can split
            for axis in range(self.dimension):
                if sz[axis] < available[axis] - 1e-8:
                    # Split along this axis
                    split = min_corner[axis] + sz[axis]
                    # Left child: [min, ..., split] (the inserted box)
                    left_bounds = self.bounds.copy()
                    left_bounds[1, axis] = split
                    # Right child: [split, ..., max] (the remainder)
                    right_bounds = self.bounds.copy()
                    right_bounds[0, axis] = split
                    self.left = RectangleBin(left_bounds)
                    self.right = RectangleBin(right_bounds)
                    return self.left.insert(sz, rotate=False)
            # If we get here, it fits but doesn't need splitting (shouldn't happen)
            self.occupied = True
            return np.stack([min_corner, min_corner + sz])
        # If none of the rotations fit
        return None
