
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
        self.bounds = np.asanyarray(bounds, dtype=np.float64)
        if self.bounds.shape[0] != 2:
            raise ValueError('bounds must be (2, dimension)')
        self.children = [None, None]

    @property
    def extents(self):
        return self.bounds[1] - self.bounds[0]

    def insert(self, size, rotate=True):
        # check to see if we are too small
        if np.any(self.extents < size):
            return None

        # are we a leaf node
        if self.children == [None, None]:
            # try to insert into our space
            if np.all(self.extents >= size):
                # we have space: split and return
                self._split(size)
                return self.bounds[0]
            # we don't have space and can't rotate: fail
            if not rotate:
                return None
            # try to insert with rotated size
            try_rotated = self.insert(size[::-1], rotate=False)
            if try_rotated is not None:
                return try_rotated
            return None
        else:
            # try to insert into our children
            try_first = self.children[0].insert(size, rotate=rotate)
            if try_first is not None:
                return try_first
            return self.children[1].insert(size, rotate=rotate)

    def _split(self, size):
        # get our extents
        extents = self.extents
        # find the axis with the most remaining space
        axis = np.argmax(extents - size)

        # split along that axis
        left = np.copy(self.bounds)
        right = np.copy(self.bounds)
        left[1, axis] = left[0, axis] + size[axis]
        right[0, axis] = left[1, axis]

        self.children = [RectangleBin(left), RectangleBin(right)]
