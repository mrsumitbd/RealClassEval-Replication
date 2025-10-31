
class SearchDumperExt:

    def dump(self, record, data):
        if not hasattr(data, '__dict__'):
            raise ValueError("Data must be an object with attributes")
        record.update(data.__dict__)
        return record

    def load(self, data, record_cls):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        record = record_cls()
        for key, value in data.items():
            setattr(record, key, value)
        return record
