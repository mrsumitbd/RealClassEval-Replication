
class Dumper:

    def dump(self, record, data):

        data.update(record.__dict__)

    def load(self, data, record_cls):

        record = record_cls()
        for key, value in data.items():
            setattr(record, key, value)
        return record
