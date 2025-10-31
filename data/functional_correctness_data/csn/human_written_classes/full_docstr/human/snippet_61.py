import six
from abc import ABCMeta, abstractmethod

@six.add_metaclass(ABCMeta)
class BudouCache:
    """Base class for cache system.
    """

    @abstractmethod
    def get(self, key):
        """Abstract method: Gets a value by a key.

        Args:
          key (str): Key to retrieve the value.

        Returns:
          Retrieved value (str or None).

        Raises:
          NotImplementedError: If it's not implemented.
        """
        raise NotImplementedError()

    @abstractmethod
    def set(self, key, val):
        """Abstract method: Sets a value in a key.

        Args:
          key (str): Key for the value.
          val (str): Value to set.

        Raises:
          NotImplementedError: If it's not implemented.
        """
        raise NotImplementedError()