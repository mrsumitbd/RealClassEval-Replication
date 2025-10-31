from typing import Tuple, List, Union
from dataclasses import dataclass

@dataclass
class AbstractComponent:
    """
    Dataclass for a regular component.

    Parameters
    ----------
    subscripts: tuple
        Tuple of length two with first argument the list of subscripts
        in the variable definition and the second argument the list of
        subscripts list that must be ignored (EXCEPT).
    ast: object
        The AbstractSyntaxTree of the component expression
    type: str (optional)
        The type of component. 'Auxiliary' by default.
    subtype: str (optional)
        The subtype of component. 'Normal' by default.

    """
    subscripts: Tuple[List[str], List[List[str]]]
    ast: object
    type: str = 'Auxiliary'
    subtype: str = 'Normal'

    def __str__(self) -> str:
        return 'AbstractComponent %s\n' % ('%s' % repr(list(self.subscripts)) if self.subscripts else '')

    def dump(self, depth=None, indent='') -> str:
        """
        Dump the component to a printable version.

        Parameters
        ----------
        depth: int (optional)
            The number of depht levels to show in the dumped output.
            Default is None which will dump everything.

        indent: str (optional)
            The indent to use for a lower level object. Default is ''.

        """
        if depth == 0:
            return self.__str__()
        return self.__str__() + '\n' + self._str_child(depth, indent)

    def _str_child(self, depth, indent) -> str:
        return str(self.ast).replace('\t', indent).replace('\n', '\n' + indent)