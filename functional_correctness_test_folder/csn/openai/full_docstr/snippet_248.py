
import json
import os
import pathlib
import configparser

# Optional imports – if unavailable, the corresponding format will not be supported
try:
    import yaml  # type: ignore
except Exception:
    yaml = None

try:
    import toml  # type: ignore
except Exception:
    toml = None


class Parser:
    '''Provide tools to parse files'''

    _SUPPORTED_EXTENSIONS = {
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
    }

    def _infer_format(self, file_path: str) -> str:
        ext = pathlib.Path(file_path).suffix.lower()
        if ext in self._SUPPORTED_EXTENSIONS:
            return self._SUPPORTED_EXTENSIONS[ext]
        raise ValueError(
            f"Cannot infer format from extension '{ext}' for file '{file_path}'")

    def _parse_content(self, content: str, fmt: str) -> dict:
        if fmt == 'json':
            return json.loads(content)
        if fmt == 'yaml':
            if yaml is None:
                raise ImportError("PyYAML is not installed")
            return yaml.safe_load(content) or {}
        if fmt == 'toml':
            if toml is None:
                raise ImportError("toml package is not installed")
            return toml.loads(content)
        if fmt == 'ini':
            parser = configparser.ConfigParser()
            parser.read_string(content)
            # Convert to a plain dict
            return {section: dict(parser[section]) for section in parser.sections()}
        raise ValueError(f"Unsupported format '{fmt}'")

    def load_from_file(self, file_path: str, format: str | None = None) -> dict:
        '''Return dict from a file config'''
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: '{file_path}'")

        if format is None:
            format = self._infer_format(file_path)
        else:
            format = format.lower()

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self._parse_content(content, format)

    def load_all_from_directory(self, directory_path: str) -> list[dict]:
        '''Return a list of dict from a directory containing files'''
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Not a directory: '{directory_path}'")

        results = []
        for entry in os.scandir(directory_path):
            if entry.is_file():
                try:
                    cfg = self.load_from_file(entry.path)
                    results.append(cfg)
                except Exception:
                    # Skip files that cannot be parsed
                    continue
        return results
