class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        """
        Serializes the given record into the provided data dictionary.
        The record is expected to be an object with a __dict__ attribute.
        The data dictionary will be updated with the record's attributes.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        if not hasattr(record, "__dict__"):
            raise TypeError("record must have a __dict__ attribute")
        data.update(record.__dict__)
        return data

    def load(self, data, record_cls):
        """
        Deserializes the given data dictionary into an instance of record_cls.
        The record_cls must be callable without arguments.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        if not callable(record_cls):
            raise TypeError("record_cls must be callable")
        obj = record_cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
