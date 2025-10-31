
class SearchDumperExt:

    def dump(self, record, data):
        # Assuming record is a dictionary and data is a key to extract from the record
        if data in record:
            return record[data]
        return None

    def load(self, data, record_cls):
        # Assuming data is a dictionary and record_cls is a class to instantiate with the data
        return record_cls(**data)
