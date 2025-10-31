class SearchDumperExt:
    def dump(self, record, data):
        base = {}
        if record is not None:
            if hasattr(record, "to_dict") and callable(getattr(record, "to_dict")):
                try:
                    base = record.to_dict()
                except Exception:
                    base = {}
            elif hasattr(record, "dict") and callable(getattr(record, "dict")):
                try:
                    base = record.dict()
                except Exception:
                    base = {}
            elif hasattr(record, "__dict__"):
                try:
                    base = {k: v for k, v in vars(
                        record).items() if not k.startswith("_")}
                except Exception:
                    base = {}
        if data is None:
            return dict(base)
        if isinstance(data, dict):
            merged = dict(base)
            merged.update(data)
            return merged
        return dict(base)

    def load(self, data, record_cls):
        if data is None:
            try:
                return record_cls()
            except Exception:
                return None

        if hasattr(record_cls, "from_dict") and callable(getattr(record_cls, "from_dict")):
            try:
                return record_cls.from_dict(data)
            except Exception:
                pass

        if hasattr(record_cls, "parse_obj") and callable(getattr(record_cls, "parse_obj")):
            try:
                return record_cls.parse_obj(data)
            except Exception:
                pass

        try:
            return record_cls(**data)
        except Exception:
            try:
                instance = record_cls()
            except Exception:
                return None
            if isinstance(data, dict):
                for k, v in data.items():
                    try:
                        setattr(instance, k, v)
                    except Exception:
                        continue
            return instance
