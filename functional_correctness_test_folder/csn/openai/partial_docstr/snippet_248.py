
import json
import csv
import os
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


class Parser:
    """Utility class for loading data from files and directories."""

    _SUPPORTED_EXTENSIONS = {
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".csv": "csv",
    }

    def load_from_file(self, file_path, format=None):
        """
        Load a single file and return its contents as a Python object.

        Parameters
        ----------
        file_path : str | Path
            Path to the file to load.
        format : str, optional
            Explicit format to use ('json', 'yaml', 'csv'). If None, the format
            is inferred from the file extension.

        Returns
        -------
        dict | list
            Parsed data. For JSON and YAML the result is a dict (or list if
            the top-level JSON/YAML structure is a list). For CSV the result
            is a list of dicts, one per row.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        ValueError
            If the format is unsupported or cannot be inferred.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine format
        if format is None:
            ext = path.suffix.lower()
            format = self._SUPPORTED_EXTENSIONS.get(ext)
            if format is None:
                raise ValueError(f"Cannot infer format from extension '{ext}'. "
                                 f"Supported extensions: {list(self._SUPPORTED_EXTENSIONS.keys())}")

        # Load based on format
        if format == "json":
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)

        if format == "yaml":
            if yaml is None:
                raise ImportError("PyYAML is required for YAML support")
            with path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f)

        if format == "csv":
            with path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                return [row for row in reader]

        raise ValueError(f"Unsupported format: {format}")

    def load_all_from_directory(self, directory_path):
        """
        Load all supported files from a directory and return a list of parsed
        objects.

        Parameters
        ----------
        directory_path : str | Path
            Path to the directory containing files to load.

        Returns
        -------
        list
            A list of parsed objects (dicts or lists) corresponding to each
            file in the directory.

        Raises
        ------
        FileNotFoundError
            If the directory does not exist.
        """
        dir_path = Path(directory_path)
        if not dir_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        results = []
        for entry in dir_path.iterdir():
            if entry.is_file() and entry.suffix.lower() in self._SUPPORTED_EXTENSIONS:
                try:
                    data = self.load_from_file(entry)
                    results.append(data)
                except Exception as exc:
                    # Skip files that cannot be parsed; optionally log the error
                    # For now, we simply ignore them.
                    pass
        return results
