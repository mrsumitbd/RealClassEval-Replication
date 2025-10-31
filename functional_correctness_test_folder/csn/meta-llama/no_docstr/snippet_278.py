
import json


class Dumper:

    def dump(self, record, data):
        """Dumps the given data into the provided record."""
        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)
            else:
                raise AttributeError(
                    f"'{type(record).__name__}' object has no attribute '{key}'")

    def load(self, data, record_cls):
        """Loads data from the given string into an instance of the provided record class."""
        try:
            data_dict = json.loads(data)
            return record_cls(**data_dict)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to load data: {e}")
