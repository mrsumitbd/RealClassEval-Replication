
import json
import yaml


class WCxf:
    def __init__(self, data):
        self.data = data

    @classmethod
    def load(cls, stream, fmt='json', **kwargs):
        if fmt == 'json':
            data = json.load(stream)
        elif fmt == 'yaml' or fmt == 'yml':
            data = yaml.safe_load(stream)
        else:
            raise ValueError(
                "Unsupported format. Supported formats are 'json', 'yaml', 'yml'.")
        return cls(data)

    def dump(self, stream=None, fmt='json', **kwargs):
        if fmt == 'json':
            data = json.dumps(self.data, **kwargs)
        elif fmt == 'yaml' or fmt == 'yml':
            data = yaml.dump(self.data, **kwargs)
        else:
            raise ValueError(
                "Unsupported format. Supported formats are 'json', 'yaml', 'yml'.")

        if stream is None:
            return data
        else:
            stream.write(data)
