
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

        # Try to detect format: JSON or YAML
        # Try JSON first
        try:
            data = json.loads(content)
            fmt = 'json'
        except Exception:
            if not has_yaml:
                raise ValueError(
                    "YAML support requires PyYAML to be installed.")
            data = yaml.safe_load(content)
            fmt = 'yaml'

        # Create an instance and set attributes
        obj = cls.__new__(cls)
        if isinstance(data, dict):
            obj.__dict__.update(data)
        else:
            obj.data = data
        obj._format = fmt
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
        # Prepare data to dump
        data = self.__dict__.copy()
        data.pop('_format', None)

        if fmt == 'json':
            if stream is None:
                return json.dumps(data, **kwargs)
            else:
                return json.dump(data, stream, **kwargs)
        elif fmt == 'yaml':
            try:
                import yaml
            except ImportError:
                raise ValueError(
                    "YAML support requires PyYAML to be installed.")
            if stream is None:
                return yaml.dump(data, **kwargs)
            else:
                return yaml.dump(data, stream, **kwargs)
        else:
            raise ValueError("Unknown format: {}".format(fmt))
