
class SearchDumperExt:

    def dump(self, record, data):
        # Add a '_search' key to data with the value of record's __dict__
        data = data.copy()
        data['_search'] = dict(record.__dict__)
        return data

    def load(self, data, record_cls):
        # Remove the '_search' key and use its value to create a record_cls instance
        data = data.copy()
        search_data = data.pop('_search', {})
        record = record_cls.__new__(record_cls)
        record.__dict__.update(search_data)
        return record
