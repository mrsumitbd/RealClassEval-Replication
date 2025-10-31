import time
from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, Union, get_args, get_origin

class Timer:
    """A context manager for timing code execution in a thread-safe manner."""

    def __init__(self) -> None:
        self.elapsed = 0.0

    def __enter__(self) -> 'Timer':
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        self.elapsed = time.perf_counter() - self.start