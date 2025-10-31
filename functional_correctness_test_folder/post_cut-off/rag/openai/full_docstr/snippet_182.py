
from __future__ import annotations

import io
from typing import TextIO, Union


class OutputSink:
    """Abstract output sink for processed markdown text."""

    def __init__(
        self,
        destination: Union[str, TextIO, None] = None,
        mode: str = "w",
        encoding: str = "utf-8",
    ) -> None:
        """
        Create a new output sink.

        Parameters
        ----------
        destination:
            If ``None`` a memory buffer is used.  If a string, it is treated as a
            file path and opened for writing.  Otherwise a file‑like object
            with a ``write`` method is used directly.
        mode:
            File mode used when ``destination`` is a path.
        encoding:
            Encoding used when ``destination`` is a path.
        """
        if destination is None:
            self._buffer: list[str] | None = []
            self._file: TextIO | None = None
        elif isinstance(destination, str):
            self._file = open(destination, mode, encoding=encoding)
            self._buffer = None
        else:
            self._file = destination
            self._buffer = None

    def write(self, text: str) -> None:
        """Write text to the sink."""
        if self._file is not None:
            self._file.write(text)
        else:
            assert self._buffer is not None
            self._buffer.append(text)

    def finalize(self) -> None:
        """Finalize the output."""
        if self._file is not None:
            self._file.flush()
            self._file.close()
        # If using a buffer, nothing special is required on finalize.
