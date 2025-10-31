class SecureSerializer:
    SAFE_MODULES = {
        "builtins",
        "math",
        "operator",
        "functools",
        "itertools",
        "statistics",
        "string",
        "re",
        "collections",
        "heapq",
        "bisect",
        "types",
    }
    RESTRICTED_MODULES = {
        "datetime",
        "time",
        "random",
        "decimal",
        "fractions",
        "json",
        "uuid",
        "dataclasses",
    }
    HIGH_RISK_MODULES = {
        "os",
        "sys",
        "subprocess",
        "socket",
        "ssl",
        "http",
        "urllib",
        "shutil",
        "ctypes",
        "multiprocessing",
        "threading",
        "concurrent",
        "pickle",
        "importlib",
        "inspect",
        "pdb",
        "atexit",
        "signal",
        "tempfile",
        "pathlib",
    }

    @staticmethod
    def _get_module_capability(module_name):
        if module_name in SecureSerializer.SAFE_MODULES:
            return "safe"
        if module_name in SecureSerializer.RESTRICTED_MODULES:
            return "restricted"
        if module_name in SecureSerializer.HIGH_RISK_MODULES:
            return "high_risk"
        return "restricted"

    @staticmethod
    def _is_safe_callable(obj):
        import types as _types

        # Only allow top-level functions or builtins with a resolvable module and qualname
        is_func = isinstance(
            obj, (_types.FunctionType, _types.BuiltinFunctionType, _types.BuiltinMethodType))
        if not is_func:
            return False
        name = getattr(obj, "__name__", None)
        qualname = getattr(obj, "__qualname__", None)
        module = getattr(obj, "__module__", None)
        if not module or not name or not qualname:
            return False
        if name == "<lambda>":
            return False
        # Must be top-level (no nested/local functions)
        if "<locals>" in qualname:
            return False
        # Ensure module capability is known
        cap = SecureSerializer._get_module_capability(module)
        return cap in {"safe", "restricted", "high_risk"}

    @staticmethod
    def _module_allowed(capability, allow_restricted, allow_high_risk):
        if capability == "safe":
            return True
        if capability == "restricted":
            return allow_restricted
        if capability == "high_risk":
            return allow_high_risk
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        import base64

        def _ser(o):
            # Primitives
            if o is None or isinstance(o, (bool, int, float, str)):
                return o
            # Bytes -> base64 with marker
            if isinstance(o, (bytes, bytearray)):
                b = bytes(o)
                return {"__type__": "bytes", "b64": base64.b64encode(b).decode("ascii")}
            # Lists
            if isinstance(o, list):
                return [_ser(v) for v in o]
            # Tuples
            if isinstance(o, tuple):
                return {"__type__": "tuple", "items": [_ser(v) for v in o]}
            # Sets
            if isinstance(o, set):
                return {"__type__": "set", "items": [_ser(v) for v in o]}
            # Dicts (string keys only)
            if isinstance(o, dict):
                ser_dict = {}
                for k, v in o.items():
                    if not isinstance(k, str):
                        raise TypeError(
                            "Only string keys are supported for dict serialization")
                    ser_dict[k] = _ser(v)
                return ser_dict
            # Callables (functions/builtins)
            if SecureSerializer._is_safe_callable(o):
                module = getattr(o, "__module__", None)
                qualname = getattr(o, "__qualname__", None)
                cap = SecureSerializer._get_module_capability(module)
                if not SecureSerializer._module_allowed(cap, allow_restricted, allow_high_risk):
                    raise ValueError(
                        f"Callable from module '{module}' not allowed by policy")
                return {"__type__": "function", "module": module, "qualname": qualname}
            # Fallback not supported
            raise TypeError(
                f"Type not supported for serialization: {type(o).__name__}")

        return _ser(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        import base64
        import importlib

        def _deser(o):
            if o is None or isinstance(o, (bool, int, float, str)):
                return o
            if isinstance(o, list):
                return [_deser(v) for v in o]
            if isinstance(o, dict):
                # Typed markers
                t = o.get("__type__")
                if t == "bytes":
                    b64 = o.get("b64")
                    if not isinstance(b64, str):
                        raise ValueError("Invalid bytes payload")
                    return base64.b64decode(b64.encode("ascii"))
                if t == "tuple":
                    items = o.get("items")
                    if not isinstance(items, list):
                        raise ValueError("Invalid tuple payload")
                    return tuple(_deser(v) for v in items)
                if t == "set":
                    items = o.get("items")
                    if not isinstance(items, list):
                        raise ValueError("Invalid set payload")
                    return set(_deser(v) for v in items)
                if t == "function":
                    module_name = o.get("module")
                    qualname = o.get("qualname")
                    if not (isinstance(module_name, str) and isinstance(qualname, str)):
                        raise ValueError("Invalid function payload")
                    cap = SecureSerializer._get_module_capability(module_name)
                    if not SecureSerializer._module_allowed(cap, allow_restricted, allow_high_risk):
                        raise ValueError(
                            f"Callable from module '{module_name}' not allowed by policy")
                    mod = importlib.import_module(module_name)
                    # Resolve qualname
                    current = mod
                    for part in qualname.split("."):
                        if not hasattr(current, part):
                            raise ValueError(
                                f"Unable to resolve function '{qualname}' in module '{module_name}'")
                        current = getattr(current, part)
                    # Validate callable safety again
                    if not SecureSerializer._is_safe_callable(current):
                        raise ValueError(
                            "Resolved object is not an allowed callable")
                    # Make sure module still matches expected
                    if getattr(current, "__module__", None) != module_name:
                        raise ValueError("Resolved callable module mismatch")
                    return current
                # Regular dict: recursively deserialize values
                return {k: _deser(v) for k, v in o.items()}
            raise TypeError(
                f"Type not supported for deserialization: {type(o).__name__}")

        return _deser(obj)
