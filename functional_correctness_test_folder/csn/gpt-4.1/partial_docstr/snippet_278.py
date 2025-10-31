
class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        data['__class__'] = record.__class__.__name__
        data.update(record.__dict__)
        return data

    def load(self, data, record_cls):
        obj = record_cls.__new__(record_cls)
        attrs = dict(data)
        attrs.pop('__class__', None)
        obj.__dict__.update(attrs)
        return obj
