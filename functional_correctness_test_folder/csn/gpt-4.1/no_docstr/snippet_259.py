
import json
import io


class WCxf:
    def __init__(self, data):
        self.data = data

    @classmethod
    def load(cls, stream, **kwargs):
        if isinstance(stream, (str, bytes)):
            # Assume it's a filename
            with open(stream, 'r', encoding=kwargs.get('encoding', 'utf-8')) as f:
                data = json.load(f, **kwargs)
        elif hasattr(stream, 'read'):
            data = json.load(stream, **kwargs)
        else:
            raise ValueError("stream must be a filename or a file-like object")
        return cls(data)

    def dump(self, stream=None, fmt='json', **kwargs):
        if fmt != 'json':
            raise ValueError("Only 'json' format is supported")
        if stream is None:
            return json.dumps(self.data, **kwargs)
        elif isinstance(stream, (str, bytes)):
            # Assume it's a filename
            with open(stream, 'w', encoding=kwargs.get('encoding', 'utf-8')) as f:
                json.dump(self.data, f, **kwargs)
        elif hasattr(stream, 'write'):
            json.dump(self.data, stream, **kwargs)
        else:
            raise ValueError(
                "stream must be None, a filename, or a file-like object")
