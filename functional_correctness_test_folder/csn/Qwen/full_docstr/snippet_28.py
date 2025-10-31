
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
        self.names = names
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
        return self.result.min_distance

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
        if name == self.names[0]:
            return self.result.b1
        elif name == self.names[1]:
            return self.result.b2
        else:
            raise ValueError(f"Name {name} not found in stored names.")

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
        if name == self.names[0]:
            return self.result.nearest_points[0]
        elif name == self.names[1]:
            return self.result.nearest_points[1]
        else:
            raise ValueError(f"Name {name} not found in stored names.")
