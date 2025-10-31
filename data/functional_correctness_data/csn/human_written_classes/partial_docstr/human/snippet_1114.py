import re
from typing import Any, Coroutine, Dict, Iterator, List, Mapping, Sequence, Type, Union

class ClassExp:
    """
    Perform regular expression matching on list of classes.
    """
    RE_SPACES = re.compile('\\s+')
    RE_PYTHON_VAR = re.compile('([A-Za-z_][A-Za-z_0-9]*)')

    def __init__(self, expression):
        self._initial_expression = expression
        self._compiled_expression = self._compile(expression)

    def _compile(self, expression):
        """
        Transform a class exp into an actual regex
        """
        x = self.RE_PYTHON_VAR.sub('(?:\\1,)', expression)
        x = self.RE_SPACES.sub('', x)
        return re.compile(x)

    def _make_string(self, objects: List[Any]) -> str:
        """
        Transforms a list of objects into a matchable string
        """
        return ''.join((x.__class__.__name__ + ',' for x in objects))

    def match(self, objects: List[Any]) -> bool:
        """
        Return True if the list of objects matches the expression.
        """
        s = self._make_string(objects)
        m = self._compiled_expression.match(s)
        return m is not None