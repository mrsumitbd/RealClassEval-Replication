from typing import TYPE_CHECKING, Any, ClassVar, NoReturn, Protocol, cast, runtime_checkable

class Cmd2AttributeWrapper:
    """Wraps a cmd2-specific attribute added to an argparse Namespace.

    This makes it easy to know which attributes in a Namespace are
    arguments from a parser and which were added by cmd2.
    """

    def __init__(self, attribute: Any) -> None:
        """Initialize Cmd2AttributeWrapper instances."""
        self.__attribute = attribute

    def get(self) -> Any:
        """Get the value of the attribute."""
        return self.__attribute

    def set(self, new_val: Any) -> None:
        """Set the value of the attribute."""
        self.__attribute = new_val