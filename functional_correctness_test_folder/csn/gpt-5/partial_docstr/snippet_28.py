class DistanceData:

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
            raise ValueError("names must be a list/tuple of two strings")
        self._names = (str(names[0]), str(names[1]))
        self._result = result
        self._name_to_idx = {self._names[0]: 0, self._names[1]: 1}

    @property
    def distance(self):
        '''
        Returns the distance between the two objects.
        Returns
        -------
        distance : float
          The euclidean distance between the objects.
        '''
        # Prefer library-provided min_distance when available
        if hasattr(self._result, "min_distance"):
            d = self._result.min_distance
            if d is not None:
                try:
                    return float(d)
                except (TypeError, ValueError):
                    pass
        # Fallback: compute from nearest points
        p1, p2 = self._get_points_pair()
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        dz = p1[2] - p2[2]
        return (dx * dx + dy * dy + dz * dz) ** 0.5

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
        idx = self._name_to_idx.get(name)
        if idx is None:
            raise ValueError(
                f"Unknown object name: {name!r}. Expected one of {self._names}")
        # Try common attribute names used by python-fcl / FCL
        # Primary: id1/id2
        if hasattr(self._result, "id1") and hasattr(self._result, "id2"):
            return int(self._result.id1 if idx == 0 else self._result.id2)
        # Alternative: b1/b2 (primitive indices)
        if hasattr(self._result, "b1") and hasattr(self._result, "b2"):
            return int(self._result.b1 if idx == 0 else self._result.b2)
        raise AttributeError(
            "DistanceResult does not provide primitive/face indices (id1/id2 or b1/b2)")

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
        idx = self._name_to_idx.get(name)
        if idx is None:
            raise ValueError(
                f"Unknown object name: {name!r}. Expected one of {self._names}")
        p1, p2 = self._get_points_pair()
        p = p1 if idx == 0 else p2
        return (float(p[0]), float(p[1]), float(p[2]))

    # Internal helpers
    def _get_points_pair(self):
        # Try result.nearest_points as ((x1,y1,z1), (x2,y2,z2))
        if hasattr(self._result, "nearest_points") and self._result.nearest_points is not None:
            npnts = self._result.nearest_points
            # Some bindings store as tuple/list of two 3D sequences
            if isinstance(npnts, (list, tuple)):
                if len(npnts) == 2 and all(isinstance(v, (list, tuple)) or hasattr(v, "__getitem__") for v in npnts):
                    p1 = self._to_xyz(npnts[0])
                    p2 = self._to_xyz(npnts[1])
                    return p1, p2
                # Or flat length-6 sequence
                if len(npnts) == 6:
                    p1 = self._to_xyz(npnts[0:3])
                    p2 = self._to_xyz(npnts[3:6])
                    return p1, p2
        # Alternative attribute names occasionally used
        for a1, a2 in (("nearest_points1", "nearest_points2"),
                       ("p1", "p2"),
                       ("point1", "point2")):
            if hasattr(self._result, a1) and hasattr(self._result, a2):
                p1 = self._to_xyz(getattr(self._result, a1))
                p2 = self._to_xyz(getattr(self._result, a2))
                return p1, p2
        raise AttributeError("DistanceResult does not provide nearest points")

    @staticmethod
    def _to_xyz(seq):
        # Convert a 3D sequence (or numpy array) to a 3-tuple of floats
        if hasattr(seq, "tolist"):
            seq = seq.tolist()
        if not hasattr(seq, "__getitem__") or len(seq) < 3:
            raise ValueError("Expected a 3D coordinate sequence")
        return (float(seq[0]), float(seq[1]), float(seq[2]))
