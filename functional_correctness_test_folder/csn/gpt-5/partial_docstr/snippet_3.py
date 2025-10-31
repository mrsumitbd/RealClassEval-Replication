class Serializable:
    '''This is the superclass of all serializable objects.'''
    _SERIAL_VERSION = 1
    _KEY_CLASS = "__class__"
    _KEY_STATE = "state"
    _KEY_VERSION = "__version__"

    def _get_state(self):
        if hasattr(self, "__getstate__"):
            return self.__getstate__()  # type: ignore[attr-defined]
        # Fallback to shallow copy of __dict__
        try:
            return dict(self.__dict__)
        except AttributeError as e:
            raise TypeError(
                f"{self.__class__.__name__} is not state-serializable") from e

    @staticmethod
    def _class_path(cls):
        return f"{cls.__module__}.{cls.__qualname__}"

    @staticmethod
    def _resolve_class(path):
        import importlib
        parts = path.split(".")
        for i in range(len(parts), 0, -1):
            module_name = ".".join(parts[:i])
            try:
                module = importlib.import_module(module_name)
                attr_path = parts[i:]
                obj = module
                for attr in attr_path:
                    obj = getattr(obj, attr)
                return obj
            except (ModuleNotFoundError, AttributeError):
                continue
        raise ImportError(f"Cannot resolve class path: {path}")

    @staticmethod
    def _is_path_like(obj):
        try:
            import os
            return isinstance(obj, (str, bytes, os.PathLike))
        except Exception:
            return isinstance(obj, (str, bytes))

    @staticmethod
    def _open_for_write(out_file):
        if Serializable._is_path_like(out_file):
            return open(out_file, "wb"), True
        return out_file, False

    @staticmethod
    def _open_for_read(in_file):
        if Serializable._is_path_like(in_file):
            return open(in_file, "rb"), True
        return in_file, False

    def save(self, out_file):
        import pickle
        payload = {
            self._KEY_VERSION: self._SERIAL_VERSION,
            self._KEY_CLASS: self._class_path(self.__class__),
            self._KEY_STATE: self._get_state(),
        }
        fh, must_close = self._open_for_write(out_file)
        try:
            pickle.dump(payload, fh, protocol=pickle.HIGHEST_PROTOCOL)
        finally:
            if must_close:
                fh.close()

    @classmethod
    def load(cls, in_file, instantiate=True):
        import pickle
        fh, must_close = cls._open_for_read(in_file)
        try:
            payload = pickle.load(fh)
        finally:
            if must_close:
                fh.close()

        if not isinstance(payload, dict) or cls._KEY_STATE not in payload:
            raise ValueError("Invalid serialization payload")

        # If only raw data desired
        if not instantiate:
            return payload.get(cls._KEY_STATE)

        return cls._instantiated_load(payload)

    @classmethod
    def _apply_state(cls, instance, state):
        if hasattr(instance, "__setstate__"):
            instance.__setstate__(state)  # type: ignore[attr-defined]
            return
        if hasattr(instance, "__dict__"):
            instance.__dict__.update(state)
            return
        raise TypeError(f"{instance.__class__.__name__} cannot accept state")

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        # Accept either already-loaded payload dict or an input file
        if isinstance(in_file, dict) and cls._KEY_STATE in in_file:
            payload = in_file
        else:
            import pickle
            fh, must_close = cls._open_for_read(in_file)
            try:
                payload = pickle.load(fh)
            finally:
                if must_close:
                    fh.close()

        if not isinstance(payload, dict):
            raise ValueError("Invalid serialization payload")

        class_path = payload.get(cls._KEY_CLASS)
        state = payload.get(cls._KEY_STATE)

        if class_path is None:
            target_cls = cls
        else:
            target_cls = cls._resolve_class(class_path)

        if not issubclass(target_cls, cls):
            raise TypeError(
                f"Serialized type {target_cls} is not a subclass of {cls}")

        # Create instance without calling __init__
        instance = target_cls.__new__(target_cls)

        # Optionally call __init__ with provided kwargs (for subclasses that expect construction)
        if kwargs:
            target_cls.__init__(instance, **kwargs)  # type: ignore[misc]

        cls._apply_state(instance, state)
        return instance
