
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
            return None

        if self.children[0] is not None:
            new_node = self.children[0].insert(size, rotate)
            if new_node is not None:
                return new_node
            return self.children[1].insert(size, rotate)

        if np.all(size <= self.extents):
            self.occupied = True
            return self

        if not rotate:
            return None

        if np.all(size[::-1] <= self.extents):
            self.occupied = True
            return self

        if np.any(size > self.extents):
            return None

        split_dim = np.argmax(self.extents - size)
        split_val = self.bounds[0, split_dim] + size[split_dim]

        self.children[0] = RectangleBin(
            [self.bounds[0], self.bounds[1].copy()])
        self.children[0].bounds[1, split_dim] = split_val

        self.children[1] = RectangleBin(
            [self.bounds[0].copy(), self.bounds[1]])
        self.children[1].bounds[0, split_dim] = split_val

        return self.children[0].insert(size, rotate)
