
import json
import os
from pathlib import Path


class JsonWriter:
    """
    A simple JSON writer that writes each row as a JSON object on a separate line.
    The `out` parameter can be a file path (string or Path) or an already opened
    file-like object supporting the `write` method.
    """

    def __init__(self, out):
        """
        Initialize the writer.

        Parameters
        ----------
        out : str, Path, or file-like
            Destination for the JSON output. If a string or Path is provided,
            a file will be opened for writing. If a file-like object is provided,
            it will be used directly.
        """
        if isinstance(out, (str, Path)):
            # Ensure parent directories exist
            path = Path(out)
            path.parent.mkdir(parents=True, exist_ok=True)
            self._file = open(path, "w", encoding="utf-8")
            self._close_on_exit = True
        else:
            # Assume file-like object
            self._file = out
            self._close_on_exit = False

    def writerow(self, row):
        """
        Write a single row to the JSON output.

        Parameters
        ----------
        row : Any
            The data to serialize. Typically a dict or list. It must be
            JSON‑serializable.
        """
        json_line = json.dumps(row, ensure_ascii=False)
        self._file.write(json_line + "\n")

    def close(self):
        """Close the underlying file if it was opened by this writer."""
        if self._close_on_exit:
            self._file.close()

    # Context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
