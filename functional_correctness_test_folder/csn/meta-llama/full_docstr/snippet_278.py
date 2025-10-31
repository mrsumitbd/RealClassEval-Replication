
import copy


class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        '''Dump a record that can be used a source document for the search engine.
        The job of this method is to create a Python dictionary from the record
        provided in the argument.
        If you overwrite this method without calling super, then you should
        ensure that you make a deep copy of the record dictionary, to avoid
        that changes to the dump affects the record.
        :param record: The record to dump.
        :param data: The initial dump data passed in by ``record.dumps()``.
        '''
        return copy.deepcopy(data)

    def load(self, data, record_cls):
        '''Load a record from the source document of a search engine hit.
        The job of this method, is to create a record of type ``record_cls``
        based on the input ``data``.
        :param data: A Python dictionary representing the data to load.
        :param records_cls: The record class to be constructed.
        :returns: A instance of ``record_cls``.
        '''
        return record_cls(data)
