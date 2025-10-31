class Parser:
    '''Provide tools to parse files
    '''

    _EXT_TO_FORMAT = {
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
        '.conf': 'ini',
    }

    def _detect_format(self, file_path, fmt):
        if fmt:
            return fmt.lower()
        import os
        _, ext = os.path.splitext(str(file_path))
        return self._EXT_TO_FORMAT.get(ext.lower())

    def _load_json(self, file_path):
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("JSON root must be an object mapping to a dict")
        return data

    def _load_yaml(self, file_path):
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise ImportError("PyYAML is required to parse YAML files") from e
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ValueError("YAML root must be a mapping to a dict")
        return data

    def _load_toml(self, file_path):
        data = None
        try:
            import tomllib  # Python 3.11+
            with open(file_path, 'rb') as f:
                data = tomllib.load(f)
        except ModuleNotFoundError:
            try:
                import toml  # type: ignore
            except Exception as e:
                raise ImportError(
                    "tomllib (py3.11+) or toml package is required to parse TOML files") from e
            with open(file_path, 'r', encoding='utf-8') as f:
                data = toml.load(f)
        if not isinstance(data, dict):
            raise ValueError("TOML root must be a mapping to a dict")
        return data

    def _load_ini(self, file_path):
        import configparser
        parser = configparser.ConfigParser()
        with open(file_path, 'r', encoding='utf-8') as f:
            parser.read_file(f)
        result = {}
        defaults = dict(parser.defaults()) if parser.defaults() else {}
        if defaults:
            result['_defaults'] = defaults
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    def load_from_file(self, file_path, format=None):
        '''Return dict from a file config
        '''
        import os
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: {file_path}")
        fmt = self._detect_format(file_path, format)
        if fmt == 'json':
            return self._load_json(file_path)
        if fmt == 'yaml':
            return self._load_yaml(file_path)
        if fmt == 'toml':
            return self._load_toml(file_path)
        if fmt == 'ini':
            return self._load_ini(file_path)
        raise ValueError(
            f"Unsupported or unknown format for file: {file_path}")

    def load_all_from_directory(self, directory_path):
        '''Return a list of dict from a directory containing files
        '''
        import os
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Not a directory: {directory_path}")
        supported_exts = set(self._EXT_TO_FORMAT.keys())
        results = []
        for name in sorted(os.listdir(directory_path)):
            path = os.path.join(directory_path, name)
            if not os.path.isfile(path):
                continue
            _, ext = os.path.splitext(name)
            if ext.lower() not in supported_exts:
                continue
            results.append(self.load_from_file(path))
        return results
