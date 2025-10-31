
import json


class WCxf:
    '''Base class for WCxf files (not meant to be used directly).'''

    @classmethod
    def load(cls, stream, **kwargs):
        '''Load the object data from a JSON or YAML file.'''
        # Try to import yaml if available
        try:
            import yaml
            has_yaml = True
        except ImportError:
            has_yaml = False

        # Read the content if stream is a file-like object
        if hasattr(stream, 'read'):
            content = stream.read()
        else:
            content = stream

        # Try JSON first
        try:
            data = json.loads(content)
            return cls._from_dict(data)
        except Exception:
            pass

        # Try YAML if available
        if has_yaml:
            try:
                data = yaml.safe_load(content)
                return cls._from_dict(data)
            except Exception:
                pass

        raise ValueError("Could not parse input as JSON or YAML.")

    @classmethod
    def _from_dict(cls, data):
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj

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
            else:
                return json.dump(data, stream, **kwargs)
        elif fmt == 'yaml':
            try:
                import yaml
            except ImportError:
                raise ImportError("PyYAML is required for YAML support.")
            if stream is None:
                return yaml.dump(data, **kwargs)
            else:
                return yaml.dump(data, stream, **kwargs)
        else:
            raise ValueError("Format must be 'json' or 'yaml'.")
