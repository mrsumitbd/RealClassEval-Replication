
class DistanceData:
    def __init__(self, names, result):
        """
        Initialize a DistanceData.
        Parameters
        ----------
        names : list of str
            The names of the two objects in order.
        result : fcl.DistanceResult
            The distance query result.
        """
        if not isinstance(names, (list, tuple)) or len(names) != 2:
            raise ValueError("names must be a list or tuple of two strings")
        self._names = list(names)
        self._result = result

        # Prepare mappings for quick lookup
        self._index_map = {}
        self._point_map = {}

        # Distance result may expose nearest_points and nearest_points_indices
        # as tuples/lists of length 2. If not present, we leave maps empty.
        try:
            points = result.nearest_points
            indices = getattr(result, "nearest_points_indices", None)
            if points is not None and len(points) == 2:
                self._point_map[self._names[0]] = tuple(points[0])
                self._point_map[self._names[1]] = tuple(points[1])
            if indices is not None and len(indices) == 2:
                self._index_map[self._names[0]] = int(indices[0])
                self._index_map[self._names[1]] = int(indices[1])
        except Exception:
            # If any attribute access fails, leave maps empty
            pass

    @property
    def distance(self):
        """
        Returns the distance between the two objects.
        Returns
        -------
        distance : float
            The euclidean distance between the objects.
        """
        return getattr(self._result, "distance", None)

    def index(self, name):
        """
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
        """
        if name not in self._names:
            raise ValueError(f"Unknown name: {name}")
        if name in self._index_map:
            return self._index_map[name]
        # If index not available, try to fetch from result directly
        try:
            indices = getattr(self._result, "nearest_points_indices", None)
            if indices is not None:
                idx = indices[self._names.index(name)]
                return int(idx)
        except Exception:
            pass
        # Fallback: return -1 to indicate unknown
        return -1

    def point(self, name):
        """
        The 3D point of closest distance on the mesh with the given name.
        Parameters
        ----------
        name : str
            The name of the target object.
        Returns
        -------
        point : (3,) float
            The closest point.
        """
        if name not in self._names:
            raise ValueError(f"Unknown name: {name}")
        if name in self._point_map:
            return self._point_map[name]
        # If point not available, try to fetch from result directly
        try:
            points = getattr(self._result, "nearest_points", None)
            if points is not None:
                pt = points[self._names.index(name)]
                return tuple(pt)
        except Exception:
            pass
        # Fallback: return None
        return None
