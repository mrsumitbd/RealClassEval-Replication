from abc import ABC, abstractmethod
import threading
from typing import Optional


class OutputSink(ABC):
    """Abstract output sink for processed markdown text."""

    def __init__(self) -> None:
        self._finalized: bool = False
        self._lock = threading.RLock()

    def write(self, text: str) -> None:
        """Write text to the sink."""
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        with self._lock:
            if self._finalized:
                raise RuntimeError("Cannot write to a finalized sink")
            self._write(text)

    def finalize(self) -> None:
        """Finalize the output."""
        with self._lock:
            if self._finalized:
                return
            self._finalized = True
            self._finalize()

    @abstractmethod
    def _write(self, text: str) -> None:
        """Subclasses implement how text is written."""
        raise NotImplementedError

    def _finalize(self) -> None:
        """Subclasses may override to flush/close resources."""
        pass

    @property
    def finalized(self) -> bool:
        return self._finalized

    def __enter__(self) -> "OutputSink":
        return self

    def __exit__(self, exc_type, exc, tb) -> Optional[bool]:
        self.finalize()
        return None
