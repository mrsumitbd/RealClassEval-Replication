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
        contact : fcl.DistanceResult
          The distance query result.
        '''
        if not isinstance(names, (list, tuple)) or len(names) != 2:
            raise ValueError(
                "names must be a list/tuple of exactly two strings")
        self._names = list(names)
        self._result = result

    @property
    def distance(self):
        '''
        Returns the distance between the two objects.
        Returns
        -------
        distance : float
          The euclidean distance between the objects.
        '''
        for attr in ('min_distance', 'distance', 'dist'):
            if hasattr(self._result, attr):
                val = getattr(self._result, attr)
                return float(val)
        raise AttributeError("Distance attribute not found on result")

    def _name_index(self, name):
        try:
            return self._names.index(name)
        except ValueError:
            raise KeyError(f"Unknown name: {name}")

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
          The index of the face in collisoin.
        '''
        i = self._name_index(name)
        candidates = [
            ('b1', 'b2'),
            ('id1', 'id2'),
            ('prim_id1', 'prim_id2'),
            ('face_id1', 'face_id2'),
            ('triangle_index1', 'triangle_index2'),
            ('closest_feature1', 'closest_feature2'),
        ]
        for a1, a2 in candidates:
            attr = a1 if i == 0 else a2
            if hasattr(self._result, attr):
                val = getattr(self._result, attr)
                if val is None:
                    continue
                try:
                    return int(val)
                except (TypeError, ValueError):
                    continue
        raise AttributeError("Face index attributes not found on result")

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
        i = self._name_index(name)

        # Array of two points
        for attr in ('nearest_points', 'closest_points', 'points'):
            if hasattr(self._result, attr):
                pts = getattr(self._result, attr)
                p = pts[i]
                return tuple(float(x) for x in p)

        # Individual point attributes
        pair_candidates = [
            ('nearest_point1', 'nearest_point2'),
            ('closest_point1', 'closest_point2'),
            ('p1', 'p2'),
            ('point1', 'point2'),
        ]
        for a1, a2 in pair_candidates:
            attr = a1 if i == 0 else a2
            if hasattr(self._result, attr):
                p = getattr(self._result, attr)
                return tuple(float(x) for x in p)

        raise AttributeError("Closest point attributes not found on result")
