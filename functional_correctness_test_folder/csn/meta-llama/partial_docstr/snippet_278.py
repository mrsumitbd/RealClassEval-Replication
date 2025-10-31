
import json


class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        """Dumps the given data into a JSON string."""
        return json.dumps(data)

    def load(self, data, record_cls):
        """Loads the given JSON string into an instance of the given record class."""
        loaded_data = json.loads(data)
        return record_cls(**loaded_data)
