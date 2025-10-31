
from dataclasses import is_dataclass, asdict
from typing import Any, Dict, Type


class SearchDumperExt:
    """
    Utility class for serialising (dumping) and deserialising (loading) objects.
    Works with plain objects, dataclasses and simple dictionaries.
    """

    def dump(self, record: Any, data: Dict[str, Any]) -> None:
        """
        Serialise the attributes of *record* into the *data* dictionary.

        Parameters
        ----------
        record : Any
            The object to serialise. It can be a dataclass instance, a plain
            object with a ``__dict__`` or a dictionary.
        data : dict
            The dictionary that will receive the serialised data. It is
            modified in‑place.

        Notes
        -----
        * Private attributes (starting with an underscore) and callables are
          ignored.
        * If *record* is a dictionary, its items are merged into *data*.
        """
        if record is None:
            return

        # If the record is already a dictionary, merge it directly.
        if isinstance(record, dict):
            data.update(record)
            return

        # If the record is a dataclass, use asdict for a clean conversion.
        if is_dataclass(record):
            data.update(asdict(record))
            return

        # Fallback: iterate over the instance's __dict__.
        for key, value in vars(record).items():
            if key.startswith("_") or callable(value):
                continue
            data[key] = value

    def load(self, data: Dict[str, Any], record_cls: Type[Any]) -> Any:
        """
        Deserialise *data* into an instance of *record_cls*.

        Parameters
        ----------
        data : dict
            The dictionary containing the serialised data.
        record_cls : type
            The class to instantiate. It can be a dataclass or any class
            that accepts keyword arguments matching the keys in *data*.

        Returns
        -------
        Any
            An instance of *record_cls* populated with the values from *data*.
            If *record_cls* cannot be instantiated with ``**data`` a fallback
            approach is used: the class is instantiated without arguments and
            attributes are set individually.

        Notes
        -----
        * If *data* is ``None`` or empty, ``None`` is returned.
        """
        if not data:
            return None

        # Try to instantiate directly with keyword arguments.
        try:
            return record_cls(**data)
        except TypeError:
            # Fallback: create an empty instance and set attributes manually.
            obj = record_cls()
            for key, value in data.items():
                setattr(obj, key, value)
            return obj
