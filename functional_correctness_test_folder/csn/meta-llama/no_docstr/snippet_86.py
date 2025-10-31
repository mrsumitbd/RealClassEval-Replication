
from typing import Any


class Cmd2AttributeWrapper:

    def __init__(self, attribute: Any) -> None:
        """
        Initializes the Cmd2AttributeWrapper instance.

        Args:
        attribute (Any): The attribute to be wrapped.
        """
        self._attribute = attribute

    def get(self) -> Any:
        """
        Retrieves the wrapped attribute.

        Returns:
        Any: The wrapped attribute.
        """
        return self._attribute

    def set(self, new_val: Any) -> None:
        """
        Sets the wrapped attribute to a new value.

        Args:
        new_val (Any): The new value for the wrapped attribute.
        """
        self._attribute = new_val
