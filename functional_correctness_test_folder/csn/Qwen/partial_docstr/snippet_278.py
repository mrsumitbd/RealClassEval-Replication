
class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        # Implement the logic to dump record and data
        return f"Dumped {record} with data {data}"

    def load(self, data, record_cls):
        # Implement the logic to load data into record_cls
        return record_cls(data)
