
import os
import json
import csv

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


class Parser:
    """
    A simple file parser that can load JSON, YAML, and CSV files.
    """

    def load_from_file(self, file_path, format=None):
        """
        Load and parse a single file.

        Parameters
        ----------
        file_path : str
            Path to the file to load.
        format : str, optional
            Explicit format to use ('json', 'yaml', 'yml', 'csv').
            If None, the format is inferred from the file extension.

        Returns
        -------
        object
            The parsed data structure.

        Raises
        ------
        ValueError
            If the format is unsupported or cannot be inferred.
        FileNotFoundError
            If the file does not exist.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if format is None:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            if ext == ".json":
                format = "json"
            elif ext in {".yaml", ".yml"}:
                format = "yaml"
            elif ext == ".csv":
                format = "csv"
            else:
                raise ValueError(f"Cannot infer format from extension '{ext}'. "
                                 f"Specify the 'format' argument.")

        format = format.lower()

        with open(file_path, "r", encoding="utf-8") as f:
            if format == "json":
                return json.load(f)
            elif format in {"yaml", "yml"}:
                if yaml is None:
                    raise ImportError("PyYAML is required for YAML parsing.")
                return yaml.safe_load(f)
            elif format == "csv":
                reader = csv.DictReader(f)
                return list(reader)
            else:
                raise ValueError(f"Unsupported format: {format}")

    def load_all_from_directory(self, directory_path):
        """
        Load and parse all supported files in a directory.

        Parameters
        ----------
        directory_path : str
            Path to the directory containing files to load.

        Returns
        -------
        dict
            Mapping from file names to parsed data structures.
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Not a directory: {directory_path}")

        results = {}
        for entry in os.scandir(directory_path):
            if entry.is_file():
                try:
                    data = self.load_from_file(entry.path)
                    results[entry.name] = data
                except Exception:
                    # Skip files that cannot be parsed
                    continue
        return results
