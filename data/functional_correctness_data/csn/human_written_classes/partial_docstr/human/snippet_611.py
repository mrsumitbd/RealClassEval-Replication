import salesforce.fields
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

class SymbolicModelsName:
    """A symbolic name from the `models` module.
    >>> from salesforce import models
    >>> assert models.READ_ONLY == 3
    >>> SymbolicModelsName('READ_ONLY').value
    3
    >>> [SymbolicModelsName('READ_ONLY')]
    [models.READ_ONLY]
    """

    def __init__(self, name: str, arg: Any=None) -> None:
        self.name = 'models.%s' % name
        self.value = getattr(salesforce.fields, name)
        if arg is not None:
            self.name = '{}({})'.format(self.name, repr(arg))
            self.value = self.value(arg)

    def __repr__(self) -> str:
        return self.name