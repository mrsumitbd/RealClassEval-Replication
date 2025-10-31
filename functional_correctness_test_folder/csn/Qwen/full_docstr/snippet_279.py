
class SearchDumperExt:
    '''Interface for Search dumper extensions.'''

    def dump(self, record, data):
        '''Dump the data.'''
        # Example implementation: Convert record to a dictionary and update data
        data.update(record.__dict__)
        return data

    def load(self, data, record_cls):
        '''Load the data.
        Reverse the changes made by the dump method.
        '''
        # Example implementation: Create an instance of record_cls using data
        return record_cls(**data)
