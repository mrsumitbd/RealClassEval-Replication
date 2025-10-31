class DistanceData:
    def __init__(self, names, result):
        """
        Initialize with a list of names and a distance matrix.

        Parameters
        ----------
        names : list of str
            The names corresponding to each row/column in the distance matrix.
        result : list of list or 2D array-like
            The distance matrix. Must be square with size equal to len(names).
        """
        if not isinstance(names, (list, tuple)):
            raise TypeError("names must be a list or tuple of strings")
        if not isinstance(result, (list, tuple)):
            raise TypeError("result must be a list or tuple of lists/arrays")
        n = len(names)
        if len(result) != n:
            raise ValueError(
                "result must have the same number of rows as names")
        for row in result:
            if len(row) != n:
                raise ValueError("result must be a square matrix")
        self._names = list(names)
        self._result = [list(row) for row in result]

    @property
    def distance(self):
        """Return the distance matrix."""
        return self._result

    def index(self, name):
        """
        Return the index of the given name.

        Parameters
        ----------
        name : str
            The name to look up.

        Returns
        -------
        int
            The index of the name in the names list.

        Raises
        ------
        ValueError
            If the name is not found.
        """
        try:
            return self._names.index(name)
        except ValueError as e:
            raise ValueError(f"Name '{name}' not found") from e

    def point(self, name):
        """
        Return the distance vector for the given name.

        Parameters
        ----------
        name : str
            The name whose distance vector to retrieve.

        Returns
        -------
        list
            The list of distances from the given name to all names.
        """
        idx = self.index(name)
        # return a copy to prevent accidental modification
        return self._result[idx][:]
