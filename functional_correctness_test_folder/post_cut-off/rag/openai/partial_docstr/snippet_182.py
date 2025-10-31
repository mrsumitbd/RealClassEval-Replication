
import sys
from typing import Optional


class OutputSink:
    """Concrete output sink for processed markdown text.

    The sink writes to a file if a path is provided, otherwise it writes to
    standard output. The `finalize` method closes the file when appropriate.
    """

    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Create a new OutputSink.

        :param file_path: Path to the output file. If None, output is written
                          to :data:`sys.stdout`.
        """
        if file_path:
            self._file = open(file_path, "w", encoding="utf-8")
        else:
            self._file = sys.stdout

    def write(self, text: str) -> None:
        """Write text to the sink."""
        if not text:
            return
        self._file.write(text)

    def finalize(self) -> None:
        """Finalize the output by closing the file if it was opened."""
        if self._file is not sys.stdout:
            try:
                self._file.flush()
            finally:
                self._file.close()
