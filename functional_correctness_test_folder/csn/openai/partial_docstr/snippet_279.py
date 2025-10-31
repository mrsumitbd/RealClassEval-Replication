
class SearchDumperExt:
    """
    A simple dumper/loader that serialises an object into a dictionary and
    reconstructs it back.  It works with plain objects (having a ``__dict__``)
    or dictionaries.  Private attributes (starting with ``_``) are ignored
    during dumping.
    """

    def dump(self, record, data):
        """
        Serialise ``record`` into the ``data`` dictionary.

        Parameters
        ----------
        record : object | dict
            The source object to serialise.  If it is a dictionary, its
            items are copied directly.  Otherwise the public attributes
            (those not starting with an underscore) are copied.
        data : dict
            The dictionary that will receive the serialised data.  Existing
            keys are overwritten.
        """
        if isinstance(record, dict):
            for key, value in record.items():
                data[key] = value
        else:
            for key, value in getattr(record, "__dict__", {}).items():
                if not key.startswith("_"):
                    data[key] = value

    def load(self, data, record_cls):
        """
        Reconstruct an instance of ``record_cls`` from the ``data`` dictionary.

        Parameters
        ----------
        data : dict
            The dictionary containing the serialised data.
        record_cls : type
            The class to instantiate.  It must accept the keys of ``data``
            as keyword arguments (e.g. a dataclass or a normal class with
            matching ``__init__`` signature).

        Returns
        -------
        object
            An instance of ``record_cls`` populated with the data.
        """
        return record_cls(**data)
