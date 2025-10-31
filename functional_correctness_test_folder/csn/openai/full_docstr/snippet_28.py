
class DistanceData:
    '''
    Data structure for holding information about a distance query.
    '''

    def __init__(self, names, result):
        '''
        Initialize a DistanceData.
        Parameters
        ----------
        names : list of str
          The names of the two objects in order.
        result : fcl.DistanceResult
          The distance query result.
        '''
        if not isinstance(names, (list, tuple)) or len(names) != 2:
            raise ValueError("names must be a list or tuple of two strings")
        self.names = list(names)
        self.result = result

    @property
    def distance(self):
        '''
        Returns the distance between the two objects.
        Returns
        -------
        distance : float
          The euclidean distance between the objects.
        '''
        return self.result.distance

    def index(self, name):
        '''
        Returns the index of the closest face for the mesh with
        the given name.
        Parameters
        ----------
        name : str
          The name of the target object.
        Returns
        -------
        index : int
          The index of the face in collision.
        '''
        try:
            idx = self.names.index(name)
        except ValueError:
            raise ValueError(f"Name '{name}' not found in {self.names}")

        # nearest_points is a tuple (point_on_obj1, point_on_obj2)
        # Each point has attributes: point (np.ndarray) and index (int)
        np_obj = self.result.nearest_points[idx]
        if not hasattr(np_obj, "index"):
            raise AttributeError(
                f"Result object for '{name}' does not contain an 'index' attribute")
        return np_obj.index

    def point(self, name):
        '''
        The 3D point of closest distance on the mesh with the given name.
        Parameters
        ----------
        name : str
          The name of the target object.
        Returns
        -------
        point : (3,) float
          The closest point.
        '''
        try:
            idx = self.names.index(name)
        except ValueError:
            raise ValueError(f"Name '{name}' not found in {self.names}")

        np_obj = self.result.nearest_points[idx]
        if not hasattr(np_obj, "point"):
            raise AttributeError(
                f"Result object for '{name}' does not contain a 'point' attribute")
        return np_obj.point
