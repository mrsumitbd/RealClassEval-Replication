import sys
from typing import Optional, TextIO


class OutputSink:
    def __init__(self, stream: Optional[TextIO] = None, auto_flush: bool = False) -> None:
        self._stream: TextIO = stream if stream is not None else sys.stdout
        self._buffer: list[str] = []
        self._finalized: bool = False
        self._auto_flush: bool = auto_flush

    def write(self, text: str) -> None:
        if self._finalized:
            raise RuntimeError(
                "Cannot write to OutputSink after finalize has been called.")
        if not isinstance(text, str):
            text = str(text)
        self._buffer.append(text)
        if self._auto_flush:
            self.finalize()

    def finalize(self) -> None:
        if self._finalized:
            return
        if self._buffer:
            data = "".join(self._buffer)
            self._stream.write(data)
            try:
                self._stream.flush()
            except Exception:
                pass
            self._buffer.clear()
        self._finalized = True
