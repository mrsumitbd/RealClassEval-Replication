
class Dumper:

    def dump(self, record, data):
        if not hasattr(record, '__dict__'):
            raise ValueError("Record must have a __dict__ attribute")
        record.__dict__.update(data)

    def load(self, data, record_cls):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        record = record_cls()
        record.__dict__.update(data)
        return record
