
import importlib
import types
from typing import Any, Dict, List, Tuple, Set

# Define a simple capability map for demonstration purposes.
# In a real system this would be loaded from configuration or metadata.
_CAPABILITY_MAP: Dict[str, str] = {
    # module_name: capability_level
    "builtins": "public",
    "math": "public",
    "json": "public",
    # Example restricted modules
    "os": "restricted",
    "subprocess": "restricted",
    # Example high risk modules
    "pickle": "high_risk",
    "marshal": "high_risk",
}


class SecureSerializer:
    """Security‑focused serialization system with capability controls for Flock objects."""

    @staticmethod
    def _get_module_capability(module_name: str) -> str:
        """Return the capability level for a module."""
        return _CAPABILITY_MAP.get(module_name, "public")

    @staticmethod
    def _is_safe_callable(obj: Any) -> bool:
        """Check if a callable is safe to serialize."""
        if not isinstance(obj, types.FunctionType):
            return False
        module_name = getattr(obj, "__module__", None)
        if module_name is None:
            return False
        cap = SecureSerializer._get_module_capability(module_name)
        return cap == "public"

    @staticmethod
    def serialize(
        obj: Any,
        allow_restricted: bool = True,
        allow_high_risk: bool = False,
    ) -> Any:
        """
        Serialize an object with capability checks.

        The serialization format is JSON‑serialisable and includes type tags for
        callables and objects that are not natively serialisable.
        """
        def _serialize(o: Any) -> Any:
            # Basic types
            if isinstance(o, (int, float, str, bool, type(None))):
                return o

            # Containers
            if isinstance(o, (list, tuple, set)):
                return {
                    "__type__": type(o).__name__,
                    "items": [_serialize(item) for item in o],
                }

            if isinstance(o, dict):
                return {
                    "__type__": "dict",
                    "items": [
                        (_serialize(k), _serialize(v)) for k, v in o.items()
                    ],
                }

            # Callables
            if isinstance(o, types.FunctionType):
                module_name = getattr(o, "__module__", None)
                if module_name is None:
                    raise ValueError("Cannot serialize anonymous function")
                cap = SecureSerializer._get_module_capability(module_name)
                if cap == "restricted" and not allow_restricted:
                    raise PermissionError(
                        f"Restricted callable {o.__name__} from module {module_name} not allowed"
                    )
                if cap == "high_risk" and not allow_high_risk:
                    raise PermissionError(
                        f"High‑risk callable {o.__name__} from module {module_name} not allowed"
                    )
                if not SecureSerializer._is_safe_callable(o):
                    raise PermissionError(
                        f"Callable {o.__name__} from module {module_name} is not safe"
                    )
                return {
                    "__type__": "callable",
                    "module": module_name,
                    "name": o.__name__,
                }

            # Objects with __dict__
            if hasattr(o, "__dict__"):
                module_name = getattr(o, "__module__", None)
                if module_name is None:
                    module_name = "builtins"
                cap = SecureSerializer._get_module_capability(module_name)
                if cap == "restricted" and not allow_restricted:
                    raise PermissionError(
                        f"Restricted object {o.__class__.__name__} from module {module_name} not allowed"
                    )
                if cap == "high_risk" and not allow_high_risk:
                    raise PermissionError(
                        f"High‑risk object {o.__class__.__name__} from module {module_name} not allowed"
                    )
                return {
                    "__type__": "object",
                    "module": module_name,
                    "class": o.__class__.__name__,
                    "state": _serialize(o.__dict__),
                }

            # Fallback: try to convert to string
            return {"__type__": "str", "value": str(o)}

        return _serialize(obj)

    @staticmethod
    def deserialize(
        data: Any,
        allow_restricted: bool = True,
        allow_high_risk: bool = False,
    ) -> Any:
        """
        Deserialize an object with capability enforcement.

        The input must be the output of :meth:`serialize`.
        """
        def _deserialize(d: Any) -> Any:
            if isinstance(d, (int, float, str, bool, type(None))):
                return d

            if isinstance(d, dict):
                t = d.get("__type__")
                if t is None:
                    return d

                if t in ("list", "tuple", "set"):
                    items = [_deserialize(item) for item in d["items"]]
                    if t == "list":
                        return items
                    if t == "tuple":
                        return tuple(items)
                    return set(items)

                if t == "dict":
                    return {
                        _deserialize(k): _deserialize(v) for k, v in d["items"]
                    }

                if t == "callable":
                    module_name = d["module"]
                    name = d["name"]
                    cap = SecureSerializer._get_module_capability(module_name)
                    if cap == "restricted" and not allow_restricted:
                        raise PermissionError(
                            f"Restricted callable {name} from module {module_name} not allowed"
                        )
                    if cap == "high_risk" and not allow_high_risk:
                        raise PermissionError(
                            f"High‑risk callable {name} from module {module_name} not allowed"
                        )
                    module = importlib.import_module(module_name)
                    return getattr(module, name)

                if t == "object":
                    module_name = d["module"]
                    class_name = d["class"]
                    cap = SecureSerializer._get_module_capability(module_name)
                    if cap == "restricted" and not allow_restricted:
                        raise PermissionError(
                            f"Restricted object {class_name} from module {module_name} not allowed"
                        )
                    if cap == "high_risk" and not allow_high_risk:
                        raise PermissionError(
                            f"High‑risk object {class_name} from module {module_name} not allowed"
                        )
                    module = importlib.import_module(module_name)
                    cls = getattr(module, class_name)
                    obj = cls.__new__(cls)
                    state = _deserialize(d["state"])
                    obj.__dict__.update(state)
                    return obj

                if t == "str":
                    return d["value"]

                # Unknown type tag: return as is
                return d

            # Fallback: return as is
            return d

        return _deserialize(data)
