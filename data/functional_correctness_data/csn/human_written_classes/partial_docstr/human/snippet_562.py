from dataclasses import dataclass
from typing import Tuple, List, Union

@dataclass
class AbstractSubscriptRange:
    """
    Dataclass for a subscript range.

    Parameters
    ----------
    name: str
        The name of the element.
    subscripts: list or str or dict
        The subscripts as a list of strings for a regular definition,
        str for a copy definition and as a dict for a GET XLS/DIRECT
        definition.
    mapping: list
        The list of subscript range that can be mapped to.

    """
    name: str
    subscripts: Union[list, str, dict]
    mapping: list

    def __str__(self) -> str:
        return 'AbstractSubscriptRange:\t%s\n\t%s\n' % (self.name, '%s <- %s' % (self.subscripts, self.mapping) if self.mapping else self.subscripts)

    def dump(self, depth=None, indent='') -> str:
        """
        Dump the subscript range to a printable version.

        Parameters
        ----------
        depth: int (optional)
            The number of depht levels to show in the dumped output.
            Default is None which will dump everything.

        indent: str (optional)
            The indent to use for a lower level object. Default is ''.

        """
        return self.__str__()