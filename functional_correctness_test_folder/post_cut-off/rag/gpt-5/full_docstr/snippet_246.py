import base64
import importlib
import inspect
from collections.abc import Mapping, Sequence
from typing import Any


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    _CAPS = {
        "builtins": "low",
        "math": "low",
        "operator": "low",
        "statistics": "low",
        "datetime": "low",
        "functools": "restricted",
        "itertools": "restricted",
        "re": "restricted",
        "pathlib": "restricted",
        "json": "restricted",
        "decimal": "restricted",
        "fractions": "restricted",
        "os": "high",
        "sys": "high",
        "subprocess": "high",
        "shlex": "high",
        "socket": "high",
        "ssl": "high",
        "http": "high",
        "urllib": "high",
        "importlib": "high",
        "pickle": "high",
        "multiprocessing": "high",
        "threading": "high",
        "asyncio": "high",
    }

    _WRAPPER_KEY = "__secure_type__"
    _WRAPPER_VER_KEY = "__secure_version__"
    _WRAPPER_VER = 1

    @staticmethod
    def _get_module_capability(module_name):
        """Get the capability level for a module."""
        if not module_name:
            return "high"
        root = module_name.split(".", 1)[0]
        return SecureSerializer._CAPS.get(root, "restricted")

    @staticmethod
    def _is_safe_callable(obj):
        """Check if a callable is safe to serialize."""
        if not callable(obj):
            return False

        # Disallow bound methods, lambdas, closures, partials, and callable instances
        if inspect.ismethod(obj):
            return False
        if inspect.isclass(obj):
            return False
        if hasattr(obj, "__call__") and not inspect.isfunction(obj) and not inspect.ismethod(obj) and not inspect.isbuiltin(obj):
            return False

        # Allow builtin functions/methods with module info
        if inspect.isbuiltin(obj):
            mod = getattr(obj, "__module__", None)
            name = getattr(obj, "__name__", None)
            return bool(mod and name)

        # Allow top-level pure functions without closures
        if inspect.isfunction(obj):
            if obj.__name__ == "<lambda>":
                return False
            # No free variables (closures)
            if obj.__closure__:
                return False
            # Must be defined at top-level (no nested qualname)
            qn = getattr(obj, "__qualname__", obj.__name__)
            if "." in qn:
                return False
            mod = getattr(obj, "__module__", None)
            return bool(mod)
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serialize an object with capability checks."""
        def cap_allowed(level: str) -> bool:
            if level == "low":
                return True
            if level == "restricted":
                return bool(allow_restricted)
            if level == "high":
                return bool(allow_high_risk)
            return False

        def serialize_inner(o: Any, visited: set[int]) -> Any:
            oid = id(o)
            # Primitives are immutable or safe and will not loop
            if isinstance(o, (str, int, float, bool, type(None))):
                return o

            if oid in visited:
                raise ValueError(
                    "Circular reference detected during serialization")
            # Only track potentially recursive containers/objects
            track = isinstance(o, (dict, list, tuple, set, bytes, bytearray)) or not isinstance(
                o, (str, int, float, bool, type(None))
            )
            if track:
                visited.add(oid)
            try:
                # Bytes
                if isinstance(o, (bytes, bytearray)):
                    return {
                        SecureSerializer._WRAPPER_KEY: "bytes",
                        SecureSerializer._WRAPPER_VER_KEY: SecureSerializer._WRAPPER_VER,
                        "data": base64.b64encode(bytes(o)).decode("ascii"),
                    }
                # Lists
                if isinstance(o, list):
                    return [serialize_inner(x, visited) for x in o]
                # Tuples
                if isinstance(o, tuple):
                    return {
                        SecureSerializer._WRAPPER_KEY: "tuple",
                        SecureSerializer._WRAPPER_VER_KEY: SecureSerializer._WRAPPER_VER,
                        "items": [serialize_inner(x, visited) for x in o],
                    }
                # Sets
                if isinstance(o, set):
                    items = [serialize_inner(x, visited) for x in o]
                    # Best effort deterministic order
                    try:
                        items.sort(key=lambda v: repr(v))
                    except Exception:
                        pass
                    return {
                        SecureSerializer._WRAPPER_KEY: "set",
                        SecureSerializer._WRAPPER_VER_KEY: SecureSerializer._WRAPPER_VER,
                        "items": items,
                    }
                # Mappings (dict-like)
                if isinstance(o, Mapping):
                    out = {}
                    for k, v in o.items():
                        if not isinstance(k, str):
                            raise TypeError(
                                "Only string dict keys are supported for secure serialization")
                        out[k] = serialize_inner(v, visited)
                    return out
                # Callable
                if callable(o) and SecureSerializer._is_safe_callable(o):
                    mod = getattr(o, "__module__", None)
                    name = getattr(o, "__name__", None)
                    level = SecureSerializer._get_module_capability(mod)
                    if not cap_allowed(level):
                        raise PermissionError(
                            f"Callable from module '{mod}' not permitted at capability '{level}'")
                    return {
                        SecureSerializer._WRAPPER_KEY: "callable",
                        SecureSerializer._WRAPPER_VER_KEY: SecureSerializer._WRAPPER_VER,
                        "module": mod,
                        "name": name,
                        "capability": level,
                    }
                # Flock-aware objects
                # Expect an explicit opt-in API to avoid accidental leakage:
                # - __flock_serialize__(self) -> state (JSON-like)
                # - Class method for deserialization (see below)
                if hasattr(o, "__flock_serialize__"):
                    cls = o.__class__
                    mod = getattr(cls, "__module__", None)
                    cls_name = getattr(cls, "__name__", None)
                    level = SecureSerializer._get_module_capability(mod)
                    if not cap_allowed(level):
                        raise PermissionError(
                            f"Flock object from module '{mod}' not permitted at capability '{level}'")
                    state = o.__flock_serialize__()
                    safe_state = serialize_inner(state, visited)
                    return {
                        SecureSerializer._WRAPPER_KEY: "flock",
                        SecureSerializer._WRAPPER_VER_KEY: SecureSerializer._WRAPPER_VER,
                        "module": mod,
                        "class": cls_name,
                        "capability": level,
                        "state": safe_state,
                    }

                # Deny everything else by default
                raise TypeError(
                    f"Unsupported type for secure serialization: {type(o)!r}")
            finally:
                if track:
                    visited.discard(oid)

        return serialize_inner(obj, set())

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        """Deserialize an object with capability enforcement."""
        def cap_allowed(level: str) -> bool:
            if level == "low":
                return True
            if level == "restricted":
                return bool(allow_restricted)
            if level == "high":
                return bool(allow_high_risk)
            return False

        def expect_wrapper(d: dict, kind: str):
            if not isinstance(d, dict):
                raise TypeError(
                    "Invalid serialized payload: expected dict wrapper")
            if d.get(SecureSerializer._WRAPPER_KEY) != kind:
                raise ValueError(f"Invalid wrapper kind; expected '{kind}'")
            ver = d.get(SecureSerializer._WRAPPER_VER_KEY)
            if ver != SecureSerializer._WRAPPER_VER:
                raise ValueError(f"Incompatible wrapper version: {ver}")
            return d

        def deserialize_inner(o: Any) -> Any:
            # Primitives
            if isinstance(o, (str, int, float, bool, type(None))):
                return o

            # Lists
            if isinstance(o, list):
                return [deserialize_inner(x) for x in o]

            # Dict or wrapper
            if isinstance(o, dict):
                wrapper_kind = o.get(SecureSerializer._WRAPPER_KEY)
                if not wrapper_kind:
                    # Regular mapping
                    out = {}
                    for k, v in o.items():
                        if not isinstance(k, str):
                            raise TypeError(
                                "Only string dict keys are supported for secure deserialization")
                        out[k] = deserialize_inner(v)
                    return out

                # Typed wrapper
                if wrapper_kind == "bytes":
                    d = expect_wrapper(o, "bytes")
                    data = d.get("data", "")
                    if not isinstance(data, str):
                        raise TypeError("Invalid bytes data")
                    return base64.b64decode(data.encode("ascii"))

                if wrapper_kind == "tuple":
                    d = expect_wrapper(o, "tuple")
                    items = d.get("items", [])
                    if not isinstance(items, list):
                        raise TypeError("Invalid tuple items")
                    return tuple(deserialize_inner(x) for x in items)

                if wrapper_kind == "set":
                    d = expect_wrapper(o, "set")
                    items = d.get("items", [])
                    if not isinstance(items, list):
                        raise TypeError("Invalid set items")
                    return set(deserialize_inner(x) for x in items)

                if wrapper_kind == "callable":
                    d = expect_wrapper(o, "callable")
                    mod = d.get("module")
                    name = d.get("name")
                    level = SecureSerializer._get_module_capability(mod)
                    if not cap_allowed(level):
                        raise PermissionError(
                            f"Callable from module '{mod}' not permitted at capability '{level}'")
                    module = importlib.import_module(mod)
                    func = getattr(module, name)
                    if not (callable(func) and SecureSerializer._is_safe_callable(func)):
                        raise PermissionError(
                            "Deserialized callable failed safety check")
                    return func

                if wrapper_kind == "flock":
                    d = expect_wrapper(o, "flock")
                    mod = d.get("module")
                    cls_name = d.get("class")
                    level = SecureSerializer._get_module_capability(mod)
                    if not cap_allowed(level):
                        raise PermissionError(
                            f"Flock object from module '{mod}' not permitted at capability '{level}'")
                    module = importlib.import_module(mod)
                    cls = getattr(module, cls_name)
                    state = deserialize_inner(d.get("state"))
                    # Try well-known constructors for Flock objects:
                    # - @classmethod __flock_deserialize__(cls, state)
                    # - @classmethod from_flock_state(cls, state)
                    # Otherwise, deny.
                    factory = getattr(cls, "__flock_deserialize__", None)
                    if callable(factory):
                        return factory(state)
                    factory = getattr(cls, "from_flock_state", None)
                    if callable(factory):
                        return factory(state)
                    raise TypeError(
                        f"Class {cls!r} does not support flock deserialization")

                raise ValueError(f"Unknown wrapper type: {wrapper_kind}")

            # Anything else is invalid
            raise TypeError(
                f"Unsupported type for secure deserialization: {type(o)!r}")

        return deserialize_inner(obj)
