
class DistanceData:

    def __init__(self, names, result):
        """
        Initialize the DistanceData object.

        Args:
            names (list): A list of names.
            result (list): A list of lists containing distance data.
        """
        self._names = names
        self._result = result

    @property
    def distance(self):
        """
        Get the distance data.

        Returns:
            list: A list of lists containing distance data.
        """
        return self._result

    def index(self, name):
        """
        Get the index of a name in the names list.

        Args:
            name (str): The name to find the index for.

        Returns:
            int: The index of the name if found, -1 otherwise.
        """
        try:
            return self._names.index(name)
        except ValueError:
            return -1

    def point(self, name):
        """
        Get the distance data point for a given name.

        Args:
            name (str): The name to get the distance data point for.

        Returns:
            list or None: The distance data point if the name is found, None otherwise.
        """
        index = self.index(name)
        if index != -1:
            return self._result[index]
        else:
            return None


# Example usage:
if __name__ == "__main__":
    names = ['A', 'B', 'C']
    result = [[0, 10, 20], [10, 0, 15], [20, 15, 0]]
    distance_data = DistanceData(names, result)
    print(distance_data.distance)
    print(distance_data.index('A'))
    print(distance_data.point('B'))
