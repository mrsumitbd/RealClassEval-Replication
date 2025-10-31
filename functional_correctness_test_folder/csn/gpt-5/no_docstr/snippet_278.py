class Dumper:
    def dump(self, record, data):
        import dataclasses
        from collections.abc import Mapping

        if data is None:
            data = {}
        elif not isinstance(data, Mapping):
            raise TypeError("data must be a mapping or None")

        # Determine how to obtain a dict representation of the record
        if hasattr(record, "to_dict") and callable(getattr(record, "to_dict")):
            payload = record.to_dict()
        elif dataclasses.is_dataclass(record):
            payload = dataclasses.asdict(record)
        elif hasattr(record, "__dict__"):
            # Shallow copy of instance attributes
            payload = dict(record.__dict__)
        else:
            raise TypeError(
                "record is not serializable: no to_dict, not a dataclass, and no __dict__")

        if not isinstance(payload, Mapping):
            raise TypeError("Serialized record must be a mapping")

        # Merge into provided data
        out = dict(data)
        out.update(payload)
        return out

    def load(self, data, record_cls):
        import dataclasses
        from collections.abc import Mapping

        if not isinstance(data, Mapping):
            raise TypeError("data must be a mapping")

        # If class provides its own constructor from dict, use it
        from_dict = getattr(record_cls, "from_dict", None)
        if callable(from_dict):
            return from_dict(dict(data))

        # Dataclass support
        if dataclasses.is_dataclass(record_cls):
            fields = {f.name for f in dataclasses.fields(record_cls)}
            init_kwargs = {k: v for k, v in data.items() if k in fields}
            return record_cls(**init_kwargs)

        # Try constructing via kwargs
        try:
            return record_cls(**data)
        except TypeError:
            # Fallback: create empty instance and set attributes
            try:
                obj = record_cls()
            except TypeError as e:
                raise TypeError(
                    f"Cannot instantiate {record_cls} without arguments and no compatible kwargs provided") from e
            for k, v in data.items():
                try:
                    setattr(obj, k, v)
                except Exception:
                    # Ignore attributes that cannot be set
                    pass
            return obj
