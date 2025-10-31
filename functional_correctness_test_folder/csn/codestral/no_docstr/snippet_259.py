
import json
import yaml


class WCxf:

    @classmethod
    def load(cls, stream, **kwargs):
        if isinstance(stream, str):
            with open(stream, 'r') as f:
                data = f.read()
        else:
            data = stream.read()

        if 'fmt' in kwargs:
            fmt = kwargs['fmt']
        else:
            fmt = 'json'

        if fmt == 'json':
            return json.loads(data)
        elif fmt == 'yaml':
            return yaml.safe_load(data)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

    def dump(self, stream=None, fmt='json', **kwargs):
        if fmt == 'json':
            data = json.dumps(self, **kwargs)
        elif fmt == 'yaml':
            data = yaml.dump(self, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

        if stream is not None:
            if isinstance(stream, str):
                with open(stream, 'w') as f:
                    f.write(data)
            else:
                stream.write(data)
        else:
            return data
