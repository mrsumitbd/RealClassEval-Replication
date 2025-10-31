
import sys
from typing import TextIO, Union


class OutputSink:
    def __init__(self, target: Union[str, TextIO, None] = None) -> None:
        """
        Create an OutputSink.

        Parameters
        ----------
        target : str | TextIO | None, optional
            If a string is provided, it is treated as a file path and the sink
            will write to that file. If a TextIO object is provided, the sink
            will write to that object. If None, the sink writes to sys.stdout.
        """
        if target is None:
            self._file: TextIO = sys.stdout
            self._close_on_finalize: bool = False
        elif isinstance(target, str):
            self._file = open(target, "w", encoding="utf-8")
            self._close_on_finalize = True
        else:
            self._file = target
            self._close_on_finalize = False

    def write(self, text: str) -> None:
        """
        Write a string to the sink.

        Parameters
        ----------
        text : str
            The text to write.
        """
        self._file.write(text)

    def finalize(self) -> None:
        """
        Finalize the sink. If the sink owns a file, it will be closed.
        """
        if self._close_on_finalize:
            self._file.close()
