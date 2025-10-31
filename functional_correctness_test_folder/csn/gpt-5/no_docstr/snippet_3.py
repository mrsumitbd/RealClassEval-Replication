class Serializable:
    def save(self, out_file):
        import pickle
        import io

        data = {
            "module": self.__class__.__module__,
            "class": self.__class__.__name__,
            "state": self.__getstate__() if hasattr(self, "__getstate__") else dict(getattr(self, "__dict__", {})),
        }

        if isinstance(out_file, (str, bytes, bytearray)):
            # If it's a path (str) or buffer (bytes/bytearray)
            if isinstance(out_file, str):
                with open(out_file, "wb") as f:
                    pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                # bytes/bytearray -> treat as buffer and return bytes
                bio = io.BytesIO()
                pickle.dump(data, bio, protocol=pickle.HIGHEST_PROTOCOL)
                if isinstance(out_file, bytearray):
                    out_file[:] = bio.getvalue()
                else:
                    # bytes are immutable; return bytes to caller by raising TypeError is unhelpful.
                    # Instead, do nothing; caller should provide a writable file-like for bytes.
                    pass
        elif hasattr(out_file, "write"):
            pickle.dump(data, out_file, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            raise TypeError(
                "out_file must be a filepath string or a writable binary file-like object")

    @classmethod
    def load(cls, in_file, instantiate=True):
        import pickle
        import io

        def _read_data(source):
            if isinstance(source, (bytes, bytearray)):
                return pickle.loads(bytes(source))
            if isinstance(source, str):
                with open(source, "rb") as f:
                    return pickle.load(f)
            if hasattr(source, "read"):
                return pickle.load(source)
            raise TypeError(
                "in_file must be a filepath string, bytes/bytearray, or a readable binary file-like object")

        if not instantiate:
            return _read_data(in_file)
        return cls._instantiated_load(in_file)

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        import pickle
        import importlib
        import io

        def _read_data(source):
            if isinstance(source, (bytes, bytearray)):
                return pickle.loads(bytes(source))
            if isinstance(source, str):
                with open(source, "rb") as f:
                    return pickle.load(f)
            if hasattr(source, "read"):
                return pickle.load(source)
            raise TypeError(
                "in_file must be a filepath string, bytes/bytearray, or a readable binary file-like object")

        data = _read_data(in_file)
        state = kwargs.get("state", data.get("state", {}))
        module_name = data.get("module")
        class_name = data.get("class")

        target_cls = cls
        if module_name and class_name:
            try:
                mod = importlib.import_module(module_name)
                loaded_cls = getattr(mod, class_name, None)
                if isinstance(loaded_cls, type):
                    target_cls = loaded_cls
            except Exception:
                pass

        obj = target_cls.__new__(target_cls)
        if hasattr(obj, "__setstate__"):
            obj.__setstate__(state)
        else:
            if hasattr(obj, "__dict__") and isinstance(state, dict):
                obj.__dict__.update(state)
        return obj
