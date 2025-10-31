
import pickle


class SearchDumperExt:

    def dump(self, record, data):
        """Dump the record into the data."""
        data['record'] = pickle.dumps(record)

    def load(self, data, record_cls):
        '''Load the data.
        Reverse the changes made by the dump method.
        '''
        if 'record' in data:
            return pickle.loads(data['record'])
        else:
            return None
