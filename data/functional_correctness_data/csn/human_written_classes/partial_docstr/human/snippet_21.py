from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, Iterable, List, Optional, Sequence, Tuple, Type, TypeGuard, TypeVar, Union, cast, overload
import weakref

class _RefMixIn:

    @property
    def ref(self) -> Optional[weakref.ReferenceType]:
        """Internal method for retrieving a reference to the training DMatrix."""
        if hasattr(self, '_ref'):
            return self._ref
        return None

    @ref.setter
    def ref(self, ref: weakref.ReferenceType) -> None:
        self._ref = ref