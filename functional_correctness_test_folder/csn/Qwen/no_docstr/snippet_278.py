
class Dumper:

    def dump(self, record, data):
        data.update(record.__dict__)
        return data

    def load(self, data, record_cls):
        return record_cls(**data)
