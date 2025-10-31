
class SearchDumperExt:

    def dump(self, record, data):

        for key, value in record.__dict__.items():
            if key in data:
                data[key] = value

    def load(self, data, record_cls):
        '''Load the data.
        Reverse the changes made by the dump method.
        '''
        record = record_cls()
        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)
        return record
