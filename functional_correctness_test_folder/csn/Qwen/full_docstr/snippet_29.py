
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
        self.size = self.bounds[1] - self.bounds[0]

    @property
    def extents(self):
        '''
        Bounding box size.
        Returns
        ----------
        extents : (dimension,) float
          Edge lengths of bounding box
        '''
        return self.size

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
        if self.occupied:
            for child in self.children:
                if child is not None:
                    result = child.insert(size, rotate)
                    if result is not None:
                        return result
            return None

        if not self._can_fit(size):
            if rotate and len(size) == 2:
                rotated_size = size[::-1]
                if self._can_fit(rotated_size):
                    return self._insert(rotated_size)
            return None

        return self._insert(size)

    def _can_fit(self, size):
        return np.all(self.size >= size)

    def _insert(self, size):
        self.occupied = True
        return self.bounds[0]

    def _split(self):
        d = np.argmax(self.size)
        split = self.bounds[0][d] + self.size[d] / 2
        child1_bounds = np.array([self.bounds[0], self.bounds[1]])
        child1_bounds[1][d] = split
        child2_bounds = np.array([self.bounds[0], self.bounds[1]])
        child2_bounds[0][d] = split
        self.children[0] = RectangleBin(child1_bounds)
        self.children[1] = RectangleBin(child2_bounds)
