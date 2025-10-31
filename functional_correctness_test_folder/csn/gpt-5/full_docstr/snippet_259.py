import json
import io
import os


class WCxf:
    '''Base class for WCxf files (not meant to be used directly).'''
    @classmethod
    def load(cls, stream, **kwargs):
        '''Load the object data from a JSON or YAML file.'''
        text = None
        close_after = False

        if hasattr(stream, 'read'):
            text = stream.read()
        elif isinstance(stream, (str, os.PathLike)):
            f = open(stream, 'r', encoding=kwargs.pop('encoding', 'utf-8'))
            try:
                text = f.read()
            finally:
                f.close()
        elif isinstance(stream, (bytes, bytearray)):
            text = stream.decode(kwargs.pop('encoding', 'utf-8'))
        else:
            raise TypeError(
                "stream must be a readable file-like object, path-like, str, or bytes")

        # Try JSON first
        data = None
        try:
            data = json.loads(text, **kwargs)
        except Exception:
            # Try YAML if available
            try:
                import yaml
            except Exception as e:
                raise ValueError(
                    "Input is not valid JSON and PyYAML is not available to parse YAML") from e
            data = yaml.safe_load(text)

        if hasattr(cls, 'from_dict') and callable(getattr(cls, 'from_dict')):
            return cls.from_dict(data)
        try:
            return cls(**data) if isinstance(data, dict) else cls(data)
        except Exception:
            return cls(data) if not isinstance(data, dict) else cls(**data)

    def dump(self, stream=None, fmt='json', **kwargs):
        '''Dump the object data to a JSON or YAML file.
        Optional arguments:
        - `stream`: if None (default), return a string. Otherwise,
          should be a writable file-like object
        - `fmt`: format, should be 'json' (default) or 'yaml'
        Additional keyword arguments will be passed to the `json.dump(s)`
        or `yaml.dump` methods.
        '''
        if hasattr(self, 'to_dict') and callable(getattr(self, 'to_dict')):
            data = self.to_dict()
        else:
            data = getattr(self, '__dict__', self)

        if fmt not in ('json', 'yaml'):
            raise ValueError("fmt must be 'json' or 'yaml'")

        if fmt == 'json':
            if stream is None:
                return json.dumps(data, **kwargs)
            else:
                if isinstance(stream, (str, os.PathLike)):
                    with open(stream, 'w', encoding=kwargs.pop('encoding', 'utf-8')) as f:
                        json.dump(data, f, **kwargs)
                elif hasattr(stream, 'write'):
                    json.dump(data, stream, **kwargs)
                else:
                    raise TypeError(
                        "stream must be a writable file-like object or path-like")
                return None

        # YAML
        try:
            import yaml
        except Exception as e:
            raise ImportError("PyYAML is required for YAML output") from e

        if stream is None:
            return yaml.safe_dump(data, **kwargs)
        else:
            if isinstance(stream, (str, os.PathLike)):
                with open(stream, 'w', encoding=kwargs.pop('encoding', 'utf-8')) as f:
                    yaml.safe_dump(data, f, **kwargs)
            elif hasattr(stream, 'write'):
                yaml.safe_dump(data, stream, **kwargs)
            else:
                raise TypeError(
                    "stream must be a writable file-like object or path-like")
            return None
