from typing import Iterator, Tuple
from typing import List, TypeVar, Generic, Union, Any, Callable

class Process:
    d: int
    variables: Union[None, Tuple[str, ...]]

    @property
    def names(self):
        try:
            return self._names_
        except:
            self._names_ = tuple((f'_x_{i}' for i in range(self.d)))
            return self._names_

    @names.setter
    def names(self, v):
        self._names_ = v