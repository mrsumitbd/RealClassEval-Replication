
class Dumper:
    def dump(self, record, data):
        """
        Populate the provided `data` dictionary with the attributes of `record`.
        If the record has a `to_dict` method, it will be used; otherwise the
        instance's `__dict__` is copied.
        """
        if hasattr(record, "to_dict") and callable(record.to_dict):
            data.update(record.to_dict())
        else:
            # Use the instance's __dict__ (works for dataclasses and plain objects)
            data.update(vars(record))

    def load(self, data, record_cls):
        """
        Create an instance of `record_cls` from the provided `data` dictionary.
        If the class has a `from_dict` classmethod, it will be used; otherwise
        the class is instantiated with keyword arguments.
        """
        if hasattr(record_cls, "from_dict") and callable(record_cls.from_dict):
            return record_cls.from_dict(data)
        return record_cls(**data)
