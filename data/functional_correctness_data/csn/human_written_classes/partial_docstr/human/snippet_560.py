import numpy as np

class UniqueDims:
    """
    Helper class to create unique dimension names for data_vars with the
    same dimension name but different coords in xarray Datasets.
    """

    def __init__(self, original_dim_name):
        self.dim_name = original_dim_name
        self.dim_prefix = self.dim_name + '_#'
        self.unique_dims = []
        self.num = 1

    def name_new_dim(self, dim_name, coords):
        """
        Returns either a new name (original_dim_name + _# + num) if the coords
        list is not in unique_dims, or the preexisting dimension name if it is.
        Parameters
        ----------
        dim_name: str
            This argument is used to verify that we are passing the right
            dimension name to the class.
        coords: list
            List of coordinates of a dimension.

        Returns
        -------
        Updated name of the original dimension.
        """
        if dim_name != self.dim_name:
            raise ValueError(f"This object is configured to process dimension {self.dim_name} and it's being passed a dimension named {dim_name}")
        if self.is_new(coords):
            new_dim_name = self.dim_prefix + str(self.num)
            self.unique_dims.append((new_dim_name, coords))
            self.num += 1
            return new_dim_name
        else:
            for y in self.unique_dims:
                if np.array_equal(coords, y[1]):
                    return y[0]

    def is_new(self, coords):
        """
        Checks if coords is already in the unique_dims list or not.

        Parameters
        ----------
        coords: list
            List of coordinates of a dimension.

        Returns
        -------
        bool
        """
        if not any(map(lambda y: np.array_equal(y[1], coords), self.unique_dims)):
            return True
        return False