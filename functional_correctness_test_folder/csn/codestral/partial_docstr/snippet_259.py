
import json
import yaml


class WCxf:
    '''Base class for WCxf files (not meant to be used directly).'''
    @classmethod
    def load(cls, stream, **kwargs):
        '''Load the object data from a JSON or YAML file.'''
        data = yaml.safe_load(stream) if kwargs.get(
            'fmt', 'json').lower() == 'yaml' else json.load(stream)
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
        if stream is None:
            if fmt.lower() == 'yaml':
                return yaml.dump(data, **kwargs)
            else:
                return json.dumps(data, **kwargs)
        else:
            if fmt.lower() == 'yaml':
                yaml.dump(data, stream, **kwargs)
            else:
                json.dump(data, stream, **kwargs)
