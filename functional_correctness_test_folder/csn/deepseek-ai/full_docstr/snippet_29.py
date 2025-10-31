
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
        self.bounds = np.array(bounds, dtype=np.float64)
        self.child = [None, None]
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
        size = np.array(size, dtype=np.float64)
        if self.occupied:
            if self.child[0] is not None:
                inserted = self.child[0].insert(size, rotate)
                if inserted is not None:
                    return inserted
            if self.child[1] is not None:
                inserted = self.child[1].insert(size, rotate)
                if inserted is not None:
                    return inserted
            return None
        else:
            if np.any(size > self.extents):
                return None
            if rotate and len(size) == 2:
                rotated_size = np.array([size[1], size[0]])
                if np.all(rotated_size <= self.extents):
                    if self._split(rotated_size):
                        return self.bounds[0]
            if self._split(size):
                return self.bounds[0]
            return None

    def _split(self, size):
        if self.occupied:
            return False
        extents = self.extents
        size = np.array(size)
        if np.any(size > extents):
            return False
        diff = extents - size
        axis = np.argmin(diff)
        if diff[axis] < 0:
            return False
        self.occupied = True
        bounds_left = np.copy(self.bounds)
        bounds_left[1, axis] = self.bounds[0, axis] + size[axis]
        bounds_right = np.copy(self.bounds)
        bounds_right[0, axis] = bounds_left[1, axis]
        self.child[0] = RectangleBin(bounds_left)
        self.child[1] = RectangleBin(bounds_right)
        return True
