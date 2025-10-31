
from typing import Any


class Cmd2AttributeWrapper:
    """
    A simple wrapper around an attribute value that allows getting and setting
    the value through dedicated methods.
    """

    def __init__(self, attribute: Any) -> None:
        """
        Initialize the wrapper with the given attribute value.

        :param attribute: The initial value to wrap.
        """
        self._attribute = attribute

    def get(self) -> Any:
        """
        Retrieve the current value of the wrapped attribute.

        :return: The current attribute value.
        """
        return self._attribute

    def set(self, new_val: Any) -> None:
        """
        Update the wrapped attribute with a new value.

        :param new_val: The new value to assign to the attribute.
        """
        self._attribute = new_val
