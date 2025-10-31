
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
        self.leaf = True

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
        if not self.leaf:
            new_node = self.children[0].insert(size, rotate)
            if new_node is not None:
                return new_node
            return self.children[1].insert(size, rotate)

        if np.all(size <= self.extents):
            if self.leaf:
                self.leaf = False
                self.children[0] = RectangleBin(
                    [self.bounds[0], self.bounds[0] + size])
                remaining_size = self.extents - size
                if rotate and remaining_size[0] < remaining_size[1]:
                    remaining_size = remaining_size[::-1]
                self.children[1] = RectangleBin(
                    [self.bounds[0] + size, self.bounds[1]])
                return self.bounds[0]
            return None

        if rotate and np.all(size[::-1] <= self.extents):
            return self.insert(size[::-1], rotate=False)

        return None
