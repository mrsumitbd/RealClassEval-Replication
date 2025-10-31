
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
        self.children = [None, None]
        self.split_axis = None

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

        # Check if the rectangle fits in the current bin
        if np.any(size > self.extents):
            if not rotate or np.any(size[::-1] > self.extents):
                return None
            else:
                size = size[::-1]

        # If the bin is not split, try to split it
        if self.children[0] is None:
            # Check if the rectangle fits exactly in the bin
            if np.allclose(size, self.extents):
                return self.bounds[0]

            # Split the bin along the longest axis
            self.split_axis = np.argmax(self.extents)

            # Split the bin into two children
            split_pos = self.bounds[0, self.split_axis] + size[self.split_axis]
            child1_bounds = self.bounds.copy()
            child1_bounds[1, self.split_axis] = split_pos
            child2_bounds = self.bounds.copy()
            child2_bounds[0, self.split_axis] = split_pos
            self.children[0] = RectangleBin(child1_bounds)
            self.children[1] = RectangleBin(child2_bounds)

            # Insert the rectangle into the first child
            return self.children[0].insert(size, rotate=False)

        # If the bin is already split, try to insert into one of the children
        for child in self.children:
            result = child.insert(size, rotate=False)
            if result is not None:
                return result

        return None
