import os
import json
import configparser
from io import StringIO
from typing import List, Dict, Optional

# Optional TOML support: prefer tomllib (3.11+), fallback to tomli or toml
try:
    import tomllib as _toml_loader  # type: ignore

    def _parse_toml(data: bytes) -> Dict:
        return _toml_loader.loads(data.decode("utf-8"))
except Exception:
    _toml_loader = None
    try:
        import tomli as _tomli  # type: ignore

        def _parse_toml(data: bytes) -> Dict:
            return _tomli.loads(data.decode("utf-8"))
    except Exception:
        _tomli = None
        try:
            import toml as _toml  # type: ignore

            def _parse_toml(data: bytes) -> Dict:
                return _toml.loads(data.decode("utf-8"))
        except Exception:
            _toml = None

            def _parse_toml(_data: bytes) -> Dict:
                raise ImportError(
                    "No TOML parser available. Install Python 3.11+, tomli, or toml.")


# Optional YAML support via PyYAML
try:
    import yaml  # type: ignore

    def _parse_yaml(text: str) -> Dict:
        return yaml.safe_load(text)
except Exception:
    yaml = None

    def _parse_yaml(_text: str) -> Dict:
        raise ImportError(
            "PyYAML is not installed. Install with: pip install pyyaml")


class Parser:
    def _detect_format_from_extension(self, file_path: str) -> Optional[str]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".json":
            return "json"
        if ext in (".yaml", ".yml"):
            return "yaml"
        if ext == ".toml":
            return "toml"
        if ext in (".ini", ".cfg", ".conf"):
            return "ini"
        return None

    def _ensure_dict(self, data, source: str) -> Dict:
        if isinstance(data, dict):
            return data
        raise ValueError(f"Parsed content from '{source}' is not a dict")

    def _load_ini(self, text: str) -> Dict:
        parser = configparser.ConfigParser()
        parser.read_file(StringIO(text))
        result = {}
        # include DEFAULT section explicitly if it has values
        default_items = dict(parser.defaults())
        if default_items:
            result["DEFAULT"] = default_items
        for section in parser.sections():
            result[section] = {k: v for k,
                               v in parser.items(section, raw=True)}
        return result

    def load_from_file(self, file_path, format=None):
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: {file_path}")

        fmt = (format or "").strip().lower() if format is not None else None
        if not fmt or fmt == "auto":
            fmt = self._detect_format_from_extension(file_path)
        if not fmt:
            raise ValueError(
                "Unable to determine file format. Provide 'format' explicitly.")

        if fmt == "json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return self._ensure_dict(data, file_path)

        if fmt == "yaml":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            data = _parse_yaml(text)
            return self._ensure_dict(data, file_path)

        if fmt == "toml":
            with open(file_path, "rb") as f:
                bdata = f.read()
            data = _parse_toml(bdata)
            return self._ensure_dict(data, file_path)

        if fmt == "ini":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            data = self._load_ini(text)
            return self._ensure_dict(data, file_path)

        raise ValueError(f"Unsupported format: {fmt}")

    def load_all_from_directory(self, directory_path):
        '''Return a list of dict from a directory containing files
        '''
        if not isinstance(directory_path, str):
            raise TypeError("directory_path must be a string")
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"No such directory: {directory_path}")

        supported_exts = {".json", ".yaml", ".yml",
                          ".toml", ".ini", ".cfg", ".conf"}
        files = [
            os.path.join(directory_path, name)
            for name in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, name))
            and os.path.splitext(name)[1].lower() in supported_exts
        ]
        files.sort()
        results: List[Dict] = []
        for path in files:
            results.append(self.load_from_file(path))
        return results
