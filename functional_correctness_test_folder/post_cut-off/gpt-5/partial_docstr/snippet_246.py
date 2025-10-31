class SecureSerializer:
    SAFE = 0
    RESTRICTED = 1
    HIGH_RISK = 2

    _CAP_MAP = {
        # Safe modules
        "builtins": SAFE,
        "math": SAFE,
        "statistics": SAFE,
        "itertools": SAFE,
        "operator": SAFE,
        "functools": SAFE,
        "string": SAFE,
        "re": SAFE,
        "json": SAFE,

        # Restricted modules
        "random": RESTRICTED,
        "datetime": RESTRICTED,
        "pathlib": RESTRICTED,
        "sys": RESTRICTED,
        "collections": RESTRICTED,
        "collections.abc": RESTRICTED,
        "decimal": RESTRICTED,
        "fractions": RESTRICTED,

        # High risk modules
        "os": HIGH_RISK,
        "subprocess": HIGH_RISK,
        "socket": HIGH_RISK,
        "selectors": HIGH_RISK,
        "multiprocessing": HIGH_RISK,
        "threading": HIGH_RISK,
        "ctypes": HIGH_RISK,
        "signal": HIGH_RISK,
        "shutil": HIGH_RISK,
        "tempfile": HIGH_RISK,
        "importlib": HIGH_RISK,
        "glob": HIGH_RISK,
        "inspect": HIGH_RISK,
        "pkgutil": HIGH_RISK,
        "pydoc": HIGH_RISK,
    }

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        if not module_name:
            return SecureSerializer.HIGH_RISK
        return SecureSerializer._CAP_MAP.get(module_name, SecureSerializer.HIGH_RISK)

    @staticmethod
    def _is_safe_callable(obj):
        import inspect
        import builtins as _builtins

        if not callable(obj):
            return False

        # Disallow bound methods, closures, partials, and local/nested functions
        if inspect.ismethod(obj):
            return False
        if hasattr(obj, "__closure__") and obj.__closure__:
            return False
        # Disallow functions defined inside other functions or with '<locals>' in qualname
        qn = getattr(obj, "__qualname__", "")
        if qn and "<locals>" in qn:
            return False

        # Allow built-in functions
        if inspect.isbuiltin(obj):
            mod = getattr(obj, "__module__", "builtins") or "builtins"
            cap = SecureSerializer._get_module_capability(mod)
            return cap == SecureSerializer.SAFE

        # Allow top-level functions only
        if inspect.isfunction(obj):
            mod = getattr(obj, "__module__", None)
            if not mod:
                return False
            # Ensure the function is reachable as a module attribute via its __name__
            name = getattr(obj, "__name__", None)
            if not name or name.startswith("<"):
                return False
            cap = SecureSerializer._get_module_capability(mod)
            return cap in (SecureSerializer.SAFE, SecureSerializer.RESTRICTED, SecureSerializer.HIGH_RISK)

        # Disallow other callable types (instances with __call__, functools.partial, etc.)
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        import base64
        import inspect

        def ser(o):
            # Primitives
            if o is None or isinstance(o, (bool, int, float, str)):
                return o

            # Bytes -> base64
            if isinstance(o, (bytes, bytearray, memoryview)):
                data = bytes(o)
                return {
                    "__type__": "bytes",
                    "encoding": "base64",
                    "data": base64.b64encode(data).decode("ascii"),
                }

            # List
            if isinstance(o, list):
                return [ser(x) for x in o]

            # Tuple
            if isinstance(o, tuple):
                return {"__type__": "tuple", "items": [ser(x) for x in o]}

            # Set
            if isinstance(o, set):
                return {"__type__": "set", "items": [ser(x) for x in o]}

            # Dict with string keys
            if isinstance(o, dict):
                out = {}
                for k, v in o.items():
                    if not isinstance(k, str):
                        raise TypeError(
                            "Only string dictionary keys are supported")
                    out[k] = ser(v)
                return out

            # Callable
            if callable(o):
                if not SecureSerializer._is_safe_callable(o):
                    raise ValueError("Callable is not safely serializable")

                mod = getattr(o, "__module__", None) or "builtins"
                cap = SecureSerializer._get_module_capability(mod)
                if cap == SecureSerializer.RESTRICTED and not allow_restricted:
                    raise PermissionError(
                        f"Restricted callable from module '{mod}' is not allowed")
                if cap == SecureSerializer.HIGH_RISK and not allow_high_risk:
                    raise PermissionError(
                        f"High-risk callable from module '{mod}' is not allowed")

                # Only allow top-level functions and builtins addressable by name
                name = getattr(o, "__name__", None)
                if not name or name.startswith("<"):
                    raise ValueError(
                        "Only top-level named callables can be serialized")

                # Store by module + attribute name
                return {
                    "__type__": "callable",
                    "module": mod,
                    "name": name,
                    "capability": cap,
                }

            raise TypeError(
                f"Type not supported for serialization: {type(o).__name__}")

        return ser(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        import base64
        import importlib

        def deser(o):
            if isinstance(o, (type(None), bool, int, float, str)):
                return o

            if isinstance(o, list):
                return [deser(x) for x in o]

            if isinstance(o, dict):
                t = o.get("__type__")
                if not t:
                    # Regular dict
                    return {k: deser(v) for k, v in o.items()}

                if t == "bytes":
                    enc = o.get("encoding")
                    if enc != "base64":
                        raise ValueError("Unsupported bytes encoding")
                    data = o.get("data")
                    if not isinstance(data, str):
                        raise ValueError("Invalid bytes payload")
                    return base64.b64decode(data.encode("ascii"))

                if t == "tuple":
                    items = o.get("items", [])
                    return tuple(deser(x) for x in items)

                if t == "set":
                    items = o.get("items", [])
                    return set(deser(x) for x in items)

                if t == "callable":
                    mod_name = o.get("module")
                    name = o.get("name")
                    if not isinstance(mod_name, str) or not isinstance(name, str):
                        raise ValueError("Invalid callable descriptor")

                    cap = SecureSerializer._get_module_capability(mod_name)
                    if cap == SecureSerializer.RESTRICTED and not allow_restricted:
                        raise PermissionError(
                            f"Restricted callable from module '{mod_name}' is not allowed")
                    if cap == SecureSerializer.HIGH_RISK and not allow_high_risk:
                        raise PermissionError(
                            f"High-risk callable from module '{mod_name}' is not allowed")

                    module = importlib.import_module(mod_name)
                    try:
                        attr = getattr(module, name)
                    except AttributeError:
                        raise ValueError(
                            f"Callable '{name}' not found in module '{mod_name}'")

                    # Final sanity: ensure it is callable and still passes basic safe check
                    if not callable(attr):
                        raise ValueError(
                            "Deserialized attribute is not callable")
                    if not SecureSerializer._is_safe_callable(attr):
                        raise ValueError(
                            "Deserialized callable is not considered safe")

                    return attr

                raise ValueError(f"Unknown serialized type marker: {t}")

            raise TypeError(
                f"Unsupported serialized structure: {type(o).__name__}")

        return deser(obj)
