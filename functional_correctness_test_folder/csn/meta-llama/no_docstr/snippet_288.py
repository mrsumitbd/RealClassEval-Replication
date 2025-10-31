
import copy


class Aspect:

    def __init__(self, id):
        """
        Initialize the Aspect object.

        Args:
        id (int): The unique identifier for the aspect.
        """
        self.id = id

    def getId(self):
        """
        Get the unique identifier for the aspect.

        Returns:
        int: The unique identifier for the aspect.
        """
        return self.id

    def clone(self):
        """
        Create a deep copy of the Aspect object.

        Returns:
        Aspect: A deep copy of the Aspect object.
        """
        return copy.deepcopy(self)
