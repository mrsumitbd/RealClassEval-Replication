from opentelemetry.util import types
from time import time_ns
from typing import Optional, Sequence, List

class Event:

    def __init__(self, name: str, attributes: types.Attributes=None, timestamp: Optional[int]=None) -> None:
        self._name = name
        self._attributes = attributes
        if timestamp is None:
            self._timestamp = time_ns()
        else:
            self._timestamp = timestamp

    @property
    def name(self) -> str:
        return self._name

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def attributes(self) -> types.Attributes:
        return self._attributes