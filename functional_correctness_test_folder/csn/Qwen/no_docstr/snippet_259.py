
import json
import yaml


class WCxf:

    @classmethod
    def load(cls, stream, **kwargs):
        fmt = kwargs.get('fmt', 'json')
        if fmt == 'json':
            data = json.load(stream)
        elif fmt == 'yaml':
            data = yaml.safe_load(stream)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
        instance = cls()
        instance.__dict__.update(data)
        return instance

    def dump(self, stream=None, fmt='json', **kwargs):
        data = self.__dict__
        if fmt == 'json':
            output = json.dumps(data, **kwargs)
        elif fmt == 'yaml':
            output = yaml.safe_dump(data, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
        if stream is not None:
            stream.write(output)
        else:
            return output
