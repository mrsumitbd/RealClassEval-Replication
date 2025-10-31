from copy import deepcopy
from collections.abc import Mapping


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
        base = deepcopy(data) if isinstance(data, Mapping) else {}

        # Extract a dict from record using common conventions
        if hasattr(record, "to_dict") and callable(getattr(record, "to_dict")):
            src = record.to_dict()
        elif hasattr(record, "dict") and callable(getattr(record, "dict")):
            # pydantic-style
            try:
                src = record.dict()
            except TypeError:
                src = record.dict  # in case it's a property
        elif hasattr(record, "as_dict") and callable(getattr(record, "as_dict")):
            src = record.as_dict()
        elif isinstance(record, Mapping):
            src = record
        else:
            raise TypeError(
                "record must be a mapping or provide to_dict()/dict()/as_dict()")

        src_copy = deepcopy(src)
        base.update(src_copy)
        return base

    def load(self, data, record_cls):
        '''Load a record from the source document of a search engine hit.
        The job of this method, is to create a record of type ``record_cls``
        based on the input ``data``.
        :param data: A Python dictionary representing the data to load.
        :param records_cls: The record class to be constructed.
        :returns: A instance of ``record_cls``.
        '''
        if not isinstance(data, Mapping):
            raise TypeError("data must be a mapping/dict")

        payload = deepcopy(data)

        # Prefer classmethods/factory methods if available
        if hasattr(record_cls, "from_dict") and callable(getattr(record_cls, "from_dict")):
            return record_cls.from_dict(payload)

        # Try common alternate constructor names
        for method_name in ("load", "loads", "from_mapping"):
            m = getattr(record_cls, method_name, None)
            if callable(m):
                try:
                    return m(payload)
                except TypeError:
                    pass

        # Try instance construction with kwargs
        try:
            return record_cls(**payload)
        except TypeError:
            pass

        # Try passing the mapping as a single positional argument
        try:
            return record_cls(payload)
        except TypeError as exc:
            raise TypeError(
                f"Could not construct {record_cls!r} from provided data") from exc
