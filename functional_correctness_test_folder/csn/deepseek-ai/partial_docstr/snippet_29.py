
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
        self.filled = False

    @property
    def extents(self):
        '''
        Return the size of the bin.
        Returns
        ------------
        extents : (dimension,) float
          Edge lengths of the bin
        '''
        return self.bounds[1] - self.bounds[0]

    def insert(self, size, rotate=True):
        '''
        Insert a rectangle into the bin.
        Parameters
        ------------
        size : (dimension,) float
          Size of the rectangle to insert
        rotate : bool
          If True, allows rotation of rectangle
        Returns
        ------------
        inserted : bool
          True if the rectangle was inserted
        offset : (dimension,) float or None
          Position of the inserted rectangle or None
        '''
        size = np.array(size, dtype=np.float64)
        if self.filled:
            return False, None
        if self.child[0] is not None:
            inserted, offset = self.child[0].insert(size, rotate)
            if inserted:
                return True, offset
            return self.child[1].insert(size, rotate)
        if np.any(size > self.extents):
            return False, None
        if np.all(size == self.extents):
            self.filled = True
            return True, self.bounds[0]
        if rotate:
            for perm in self._permutations(size):
                inserted, offset = self._try_insert(perm)
                if inserted:
                    return True, offset
            return False, None
        else:
            return self._try_insert(size)

    def _try_insert(self, size):
        if np.any(size > self.extents):
            return False, None
        diff = self.extents - size
        split_axis = np.argmin(diff)
        split_pos = size[split_axis]
        split_bounds = np.array(self.bounds)
        split_bounds[1][split_axis] = self.bounds[0][split_axis] + split_pos
        self.child[0] = RectangleBin(split_bounds)
        split_bounds = np.array(self.bounds)
        split_bounds[0][split_axis] = self.bounds[0][split_axis] + split_pos
        self.child[1] = RectangleBin(split_bounds)
        return self.child[0].insert(size, rotate=False)

    def _permutations(self, size):
        dim = len(size)
        perms = []
        for perm in [size, size[::-1]]:
            perms.append(perm)
            if dim == 3:
                perms.append(np.array([perm[1], perm[0], perm[2]]))
                perms.append(np.array([perm[0], perm[2], perm[1]]))
                perms.append(np.array([perm[2], perm[1], perm[0]]))
                perms.append(np.array([perm[1], perm[2], perm[0]]))
                perms.append(np.array([perm[2], perm[0], perm[1]]))
        return perms
