
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
        self.bounds = np.array(bounds)
        self.children = [None, None]
        self.occupied = False

    @property
    def extents(self):
        return self.bounds[1] - self.bounds[0]

    def insert(self, size, rotate=True):
        if self.occupied:
            for child in self.children:
                if child is not None:
                    result = child.insert(size, rotate)
                    if result is not None:
                        return result
            return None

        if np.any(size > self.extents):
            if rotate and len(size) == 2:
                rotated_size = size[::-1]
                if np.any(rotated_size > self.extents):
                    return None
                else:
                    size = rotated_size
            else:
                return None

        if self.children[0] is None and self.children[1] is None:
            self.occupied = True
            return self.bounds[0]

        if self.children[0] is None:
            self.children[0] = RectangleBin(
                [self.bounds[0], self.bounds[0] + size])
            self.children[1] = RectangleBin(
                [self.bounds[0] + size, self.bounds[1]])
        return self.children[0].insert(size, rotate)
