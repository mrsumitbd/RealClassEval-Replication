
import os
from pathlib import Path
from typing import List, Tuple


class BaseLoader:
    """Base class for File Loaders"""

    def __init__(self, source_dir: str | Path):
        """
        Parameters
        ----------
        source_dir : str | Path
            Directory that contains query files.  The directory must exist.
        """
        self.source_dir = Path(source_dir).expanduser().resolve()
        if not self.source_dir.is_dir():
            raise ValueError(
                f"Source directory {self.source_dir!s} does not exist or is not a directory")

    def getTextForName(self, query_name: str) -> Tuple[str, str]:
        """
        Return the query text and query type for the given query name.

        The file extension is not part of the query name.  For example,
        for ``query_name='query1'`` this will return the content of
        ``query1.rq`` from the loader's source (assuming such file exists).

        Parameters
        ----------
        query_name : str
            Name of the query without extension.

        Returns
        -------
        tuple
            ``(text, query_type)`` where ``text`` is the file contents and
            ``query_type`` is the file extension without the leading dot.

        Raises
        ------
        FileNotFoundError
            If the query file cannot be found.
        """
        # Build the expected file path
        file_path = self.source_dir / f"{query_name}.rq"
        if not file_path.is_file():
            raise FileNotFoundError(f"Query file {file_path!s} not found")
        return self._getText(file_path)

    def _getText(self, queryFullName: str | Path) -> Tuple[str, str]:
        """
        Internal helper to read a file and return its contents and type.

        Parameters
        ----------
        queryFullName : str | Path
            Full path to the query file.

        Returns
        -------
        tuple
            ``(text, query_type)`` where ``text`` is the file contents and
            ``query_type`` is the file extension without the leading dot.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """
        path = Path(queryFullName).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"File {path!s} not found")
        text = path.read_text(encoding="utf-8")
        query_type = path.suffix.lstrip(".")
        return text, query_type

    def fetchFiles(self) -> List[str]:
        """
        Return a list of available query names (without extensions).

        Returns
        -------
        list[str]
            List of query names found in the source directory.
        """
        return [p.stem for p in self.source_dir.glob("*.rq") if p.is_file()]
