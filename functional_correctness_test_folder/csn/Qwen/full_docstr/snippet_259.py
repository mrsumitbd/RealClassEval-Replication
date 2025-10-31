
import json
import yaml


class WCxf:
    '''Base class for WCxf files (not meant to be used directly).'''
    @classmethod
    def load(cls, stream, **kwargs):
        '''Load the object data from a JSON or YAML file.'''
        if isinstance(stream, str):
            with open(stream, 'r') as f:
                data = f.read()
        else:
            data = stream.read()

        if data.strip().startswith('{'):
            return cls(**json.loads(data, **kwargs))
        else:
            return cls(**yaml.safe_load(data, **kwargs))

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
                json.dump(data, stream, **kwargs)
        elif fmt == 'yaml':
            if stream is None:
                return yaml.dump(data, **kwargs)
            else:
                yaml.dump(data, stream, **kwargs)
        else:
            raise ValueError("Format must be 'json' or 'yaml'")
