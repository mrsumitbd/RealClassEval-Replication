class Parser:
    def __init__(self):
        self._ext_to_format = {
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
            ".ini": "ini",
            ".cfg": "ini",
            ".conf": "ini",
            ".csv": "csv",
            ".txt": "text",
        }

    def load_from_file(self, file_path, format=None):
        import os

        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: {file_path}")

        fmt = (format or self._detect_format(file_path)) or "text"
        fmt = fmt.lower()
        parser = self._get_parser(fmt)
        return parser(file_path)

    def load_all_from_directory(self, directory_path):
        import os

        if not isinstance(directory_path, str):
            raise TypeError("directory_path must be a string")
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"No such directory: {directory_path}")

        results = {}
        for name in os.listdir(directory_path):
            path = os.path.join(directory_path, name)
            if not os.path.isfile(path):
                continue
            fmt = self._detect_format(name)
            if not fmt:
                continue
            try:
                results[name] = self.load_from_file(path, fmt)
            except Exception:
                continue
        return results

    def _detect_format(self, file_path):
        import os

        _, ext = os.path.splitext(file_path)
        return self._ext_to_format.get(ext.lower())

    def _get_parser(self, fmt):
        parsers = {
            "json": self._parse_json,
            "yaml": self._parse_yaml,
            "toml": self._parse_toml,
            "ini": self._parse_ini,
            "csv": self._parse_csv,
            "text": self._parse_text,
        }
        if fmt not in parsers:
            raise ValueError(f"Unsupported format: {fmt}")
        return parsers[fmt]

    def _parse_json(self, file_path):
        import json

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _parse_yaml(self, file_path):
        try:
            import yaml  # PyYAML
        except Exception as e:
            raise ImportError("PyYAML is required to parse YAML") from e
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _parse_toml(self, file_path):
        try:
            import tomllib  # Python 3.11+
            with open(file_path, "rb") as f:
                return tomllib.load(f)
        except ModuleNotFoundError:
            try:
                import toml  # Third-party fallback
            except Exception as e:
                raise ImportError(
                    "tomllib (py>=3.11) or toml package is required to parse TOML") from e
            with open(file_path, "r", encoding="utf-8") as f:
                return toml.load(f)

    def _parse_ini(self, file_path):
        import configparser

        parser = configparser.ConfigParser()
        with open(file_path, "r", encoding="utf-8") as f:
            parser.read_file(f)
        result = {}
        if parser.defaults():
            result["DEFAULT"] = dict(parser.defaults())
        for section in parser.sections():
            result[section] = {k: v for k, v in parser.items(section)}
        return result

    def _parse_csv(self, file_path):
        import csv

        with open(file_path, "r", encoding="utf-8", newline="") as f:
            sample = f.read(4096)
            f.seek(0)
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
            except csv.Error:
                dialect = csv.excel
            try:
                has_header = sniffer.has_header(sample)
            except csv.Error:
                has_header = True
            reader = csv.reader(f, dialect)
            rows = list(reader)
            if not rows:
                return []
            if has_header:
                headers = rows[0]
                return [dict(zip(headers, r)) for r in rows[1:]]
            return rows

    def _parse_text(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
