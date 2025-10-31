import numpy as np

class RectangleBin:
    """
    An N-dimensional binary space partition tree for packing
    hyper-rectangles. Split logic is pure `numpy` but behaves
    similarly to `scipy.spatial.Rectangle`.

    Mostly useful for packing 2D textures and 3D boxes and
    has not been tested outside of 2 and 3 dimensions.

    Original article about using this for packing textures:
    http://www.blackpawn.com/texts/lightmaps/
    """

    def __init__(self, bounds):
        """
        Create a rectangular bin.

        Parameters
        ------------
        bounds : (2, dimension *) float
          Bounds array are `[mins, maxes]`
        """
        self.child = []
        self.occupied = False
        self.bounds = np.array(bounds, dtype=np.float64)

    @property
    def extents(self):
        """
        Bounding box size.

        Returns
        ----------
        extents : (dimension,) float
          Edge lengths of bounding box
        """
        bounds = self.bounds
        return bounds[1] - bounds[0]

    def insert(self, size, rotate=True):
        """
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
        """
        for child in self.child:
            attempt = child.insert(size=size, rotate=rotate)
            if attempt is not None:
                return attempt
        if self.occupied:
            return None
        bounds = self.bounds.copy()
        extents = bounds[1] - bounds[0]
        if rotate:
            for roll in range(len(size)):
                size_test = extents - _roll(size, roll)
                fits = (size_test > -_TOL_ZERO).all()
                if fits:
                    size = _roll(size, roll)
                    break
            if not fits:
                return None
        else:
            size_test = extents - size
            if (size_test < -_TOL_ZERO).any():
                return None
        self.occupied = True
        if (size_test < _TOL_ZERO).all():
            return bounds
        axis = size_test.argmax()
        splits = np.vstack((bounds, bounds))
        splits[1:3, axis] = bounds[0][axis] + size[axis]
        self.child[:] = (RectangleBin(splits[:2]), RectangleBin(splits[2:]))
        return self.child[0].insert(size, rotate=rotate)