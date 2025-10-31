class DataSetProperties:

    def __init__(self, name, num_of_records, record_size):
        self.name = name
        self.num_of_records = num_of_records
        self.record_size = record_size

    def __repr__(self):
        return 'DataSetProperties({0}, {1}, {2})'.format(self.name, self.num_of_records, self.record_size)