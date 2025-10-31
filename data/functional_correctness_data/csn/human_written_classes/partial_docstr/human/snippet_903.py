from collections.abc import Iterable
from typing import Optional

class VariableFactory:
    """
    Simple class to produce variables by incrementing the variable id.

    This class is intended to be used when creating an MRS from a
    variable-less representation like DMRS where the variable types
    are known but no variable id is assigned.

    Args:
        starting_vid (int): the id of the first variable
    Attributes:
        vid (int): the id of the next variable produced by :meth:`new`
        index (dict): a mapping of ids to variables
        store (dict): a mapping of variables to associated properties
    """
    vid: int
    index: dict[int, str]
    store: dict[str, list[tuple[str, str]]]

    def __init__(self, starting_vid: int=1):
        self.vid = starting_vid
        self.index = {}
        self.store = {}

    def new(self, type: Optional[str], properties: Optional[Iterable[tuple[str, str]]]=None) -> str:
        """
        Create a new variable for the given *type*.

        Args:
            type (str): the type of the variable to produce
            properties (list): properties to associate with the variable
        Returns:
            A (variable, properties) tuple
        """
        if type is None:
            type = UNSPECIFIC
        vid, index = (self.vid, self.index)
        while vid in index:
            vid += 1
        varstring = f'{type}{vid}'
        index[vid] = varstring
        if properties is None:
            properties = []
        self.store[varstring] = list(properties)
        self.vid = vid + 1
        return varstring