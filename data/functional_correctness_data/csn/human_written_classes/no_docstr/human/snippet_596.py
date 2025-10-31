from opentelemetry.trace import format_span_id, format_trace_id, get_current_span
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Tuple, Type, TypeVar, Union
from opentelemetry.util.types import Attributes, AttributeValue

@dataclass(frozen=True)
class Exemplar:
    value: Union[int, float]
    attributes: Attributes
    time_unix_nano: int
    _trace_id: int
    _span_id: int

    @property
    def trace_id(self) -> str:
        return format_trace_id(self._trace_id) or ''

    @property
    def span_id(self) -> str:
        return format_span_id(self._span_id) or ''