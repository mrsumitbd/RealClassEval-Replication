
class WCxf:

    @classmethod
    def load(cls, stream, **kwargs):
        import json
        if hasattr(stream, 'read'):
            data = json.load(stream)
        else:
            with open(stream, 'r') as f:
                data = json.load(f)
        return cls(**data)

    def dump(self, stream=None, fmt='json', **kwargs):
        import json
        data = self.__dict__
        if fmt == 'json':
            if stream is None:
                return json.dumps(data, **kwargs)
            else:
                if hasattr(stream, 'write'):
                    json.dump(data, stream, **kwargs)
                else:
                    with open(stream, 'w') as f:
                        json.dump(data, f, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
