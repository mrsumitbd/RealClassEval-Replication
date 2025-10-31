
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
        self.bounds = np.array(bounds, dtype=float)
        self.dimension = self.bounds.shape[1]
        self.left = None
        self.right = None
        self.occupied = False

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
        size = np.array(size, dtype=float)
        # If this node has children, try to insert into them
        if self.left is not None and self.right is not None:
            res = self.left.insert(size, rotate)
            if res is not None:
                return res
            return self.right.insert(size, rotate)

        # If already occupied, cannot insert here
        if self.occupied:
            return None

        # Try all rotations if allowed
        rotations = [size]
        if rotate:
            # All unique permutations of size
            rotations = set(tuple(s) for s in itertools.permutations(size))
            rotations = [np.array(s) for s in rotations]

        for sz in rotations:
            if np.all(sz <= self.extents):
                # Perfect fit
                if np.allclose(sz, self.extents):
                    self.occupied = True
                    return self.bounds[0].copy()
                # Need to split
                # Find the first dimension where the size doesn't match
                for axis in range(self.dimension):
                    if sz[axis] < self.extents[axis]:
                        break
                else:
                    axis = 0  # fallback, should not happen

                # Split along axis
                split = self.bounds[0].copy()
                split[axis] += sz[axis]

                # Left child: the region occupied by the inserted rectangle
                left_bounds = np.array([self.bounds[0], self.bounds[1]])
                left_bounds[1][axis] = split[axis]
                self.left = RectangleBin(left_bounds)

                # Right child: the remaining region
                right_bounds = np.array([self.bounds[0], self.bounds[1]])
                right_bounds[0][axis] = split[axis]
                self.right = RectangleBin(right_bounds)

                return self.left.insert(sz, rotate=False)
        # No fit found
        return None
