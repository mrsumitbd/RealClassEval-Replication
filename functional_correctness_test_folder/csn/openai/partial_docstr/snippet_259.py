
import json
import os

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


class WCxf:
    '''Base class for WCxf files (not meant to be used directly).'''

    @classmethod
    def load(cls, stream, **kwargs):
        '''Load the object data from a JSON or YAML file.'''
        # Determine if stream is a path or a file-like object
        if isinstance(stream, str):
            # Treat as file path
            path = stream
            if not os.path.exists(path):
                raise FileNotFoundError(f"No such file: {path}")
            with open(path, 'r', encoding=kwargs.get('encoding', 'utf-8')) as f:
                content = f.read()
            # Detect format from extension
            _, ext = os.path.splitext(path.lower())
            if ext == '.json':
                data = json.loads(content, **kwargs)
            elif ext in {'.yaml', '.yml'}:
                if yaml is None:
                    raise ImportError("PyYAML is required to load YAML files")
                data = yaml.safe_load(content)
            else:
                # Try JSON first, then YAML
                try:
                    data = json.loads(content, **kwargs)
                except Exception:
                    if yaml is None:
                        raise ImportError(
                            "PyYAML is required to load YAML files")
                    data = yaml.safe_load(content)
        else:
            # Assume file-like object
            try:
                data = json.load(stream, **kwargs)
            except Exception:
                if yaml is None:
                    raise ImportError("PyYAML is required to load YAML files")
                stream.seek(0)
                data = yaml.safe_load(stream)

        if not isinstance(data, dict):
            raise ValueError("Loaded data must be a dictionary")
        return cls(**data)

    def dump(self, stream=None, fmt='json', **kwargs):
        '''Dump the object data to a JSON or YAML file.
        Optional arguments:
        - `stream`: if None (default), return a string. Otherwise,
          should be a writable file-like object
        - `fmt`: format, should be 'json' (default) or 'yaml'
        Additional keyword arguments will be passed to the `json.dump(s)`
        or `yaml.dump` methods.
        '''
        data = self.__dict__
        if fmt == 'json':
            if stream is None:
                return json.dumps(data, **kwargs)
            json.dump(data, stream, **kwargs)
        elif fmt == 'yaml':
            if yaml is None:
                raise ImportError("PyYAML is required to dump YAML files")
            if stream is None:
                return yaml.safe_dump(data, **kwargs)
            yaml.safe_dump(data, stream, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
