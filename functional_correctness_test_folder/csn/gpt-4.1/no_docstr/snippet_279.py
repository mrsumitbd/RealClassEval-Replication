
class SearchDumperExt:

    def dump(self, record, data):
        result = data.copy() if isinstance(data, dict) else {}
        if hasattr(record, '__dict__'):
            result.update(record.__dict__)
        elif isinstance(record, dict):
            result.update(record)
        return result

    def load(self, data, record_cls):
        if isinstance(data, dict):
            return record_cls(**data)
        return record_cls(data)
