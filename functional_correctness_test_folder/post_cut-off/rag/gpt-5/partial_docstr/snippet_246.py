from __future__ import annotations

import base64
import importlib
import inspect
from types import BuiltinFunctionType, FunctionType
from typing import Any


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    _SAFE_MODULES = {
        "builtins",
        "math",
        "operator",
        "functools",
        "itertools",
        "statistics",
    }
    _RESTRICTED_MODULES = {
        "datetime",
        "decimal",
        "fractions",
        "uuid",
        "collections",
        "pathlib",
        "re",
        "typing",
        "types",
        "json",
        "flock",  # presumed external library; treated as restricted by default
    }
    _HIGH_RISK_MODULES = {
        "os",
        "sys",
        "subprocess",
        "importlib",
        "ctypes",
        "multiprocessing",
        "shlex",
        "tempfile",
        "socket",
        "ssl",
    }

    _SAFE_BUILTIN_CALLABLES = {
        "abs",
        "all",
        "any",
        "ascii",
        "bin",
        "bool",
        "bytes",
        "callable",
        "chr",
        "complex",
        "dict",
        "dir",
        "divmod",
        "enumerate",
        "filter",
        "float",
        "format",
        "frozenset",
        "getattr",
        "hasattr",
        "hash",
        "hex",
        "int",
        "isinstance",
        "issubclass",
        "iter",
        "len",
        "list",
        "map",
        "max",
        "min",
        "next",
        "oct",
        "ord",
        "pow",
        "print",
        "range",
        "repr",
        "reversed",
        "round",
        "set",
        "slice",
        "sorted",
        "str",
        "sum",
        "tuple",
        "zip",
    }

    @staticmethod
    def _get_module_capability(module_name: str | None) -> str:
        """Get the capability level for a module."""
        if not module_name:
            return "high_risk"
        if module_name in SecureSerializer._SAFE_MODULES:
            return "safe"
        if module_name in SecureSerializer._RESTRICTED_MODULES:
            return "restricted"
        if module_name in SecureSerializer._HIGH_RISK_MODULES:
            return "high_risk"
        # Default: treat unknown modules as restricted to avoid overly-permissive behavior
        return "restricted"

    @staticmethod
    def _is_safe_callable(obj: Any) -> bool:
        """Check if a callable is safe to serialize."""
        if not callable(obj):
            return False

        # For built-in functions: allow only a conservative allowlist
        if isinstance(obj, BuiltinFunctionType):
            name = getattr(obj, "__name__", "")
            return name in SecureSerializer._SAFE_BUILTIN_CALLABLES

        # For Python functions: only allow top-level, non-lambda, no closures, not from __main__
        if isinstance(obj, FunctionType):
            if getattr(obj, "__name__", "") == "<lambda>":
                return False
            qn = getattr(obj, "__qualname__", "")
            if "<locals>" in qn:
                return False
            if getattr(obj, "__module__", None) in {None, "__main__"}:
                return False
            closure = getattr(obj, "__closure__", None)
            if closure:
                return False
            return True

        # Disallow bound methods, partials, instances with __call__, and other complex callables
        return False

    @staticmethod
    def serialize(obj: Any, allow_restricted: bool = True, allow_high_risk: bool = False) -> Any:
        """Serialize an object with capability checks."""
        def ser(value: Any) -> Any:
            # Primitives
            if value is None or isinstance(value, (bool, int, float, str)):
                return value

            # Bytes
            if isinstance(value, (bytes, bytearray, memoryview)):
                b = bytes(value)
                return {"__type__": "bytes", "base64": base64.b64encode(b).decode("ascii")}

            # Lists
            if isinstance(value, list):
                return {"__type__": "list", "items": [ser(v) for v in value]}

            # Tuples
            if isinstance(value, tuple):
                return {"__type__": "tuple", "items": [ser(v) for v in value]}

            # Sets
            if isinstance(value, set):
                return {"__type__": "set", "items": [ser(v) for v in value]}

            # Dicts
            if isinstance(value, dict):
                items = []
                for k, v in value.items():
                    items.append([ser(k), ser(v)])
                return {"__type__": "dict", "items": items}

            # Callables
            if SecureSerializer._is_safe_callable(value):
                module_name = getattr(value, "__module__", None)
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == "restricted" and not allow_restricted:
                    raise ValueError(
                        f"Serialization blocked: callable from restricted module '{module_name}'")
                if capability == "high_risk" and not allow_high_risk:
                    raise ValueError(
                        f"Serialization blocked: callable from high-risk module '{module_name}'")

                qualname = getattr(value, "__qualname__",
                                   getattr(value, "__name__", None))
                name = getattr(value, "__name__", qualname)
                return {
                    "__type__": "callable",
                    "module": module_name,
                    "qualname": qualname,
                    "name": name,
                }

            # Unsupported type
            typename = type(value).__name__
            module_name = getattr(type(value), "__module__", None)
            capability = SecureSerializer._get_module_capability(module_name)
            if capability == "high_risk" and not allow_high_risk:
                raise TypeError(
                    f"Serialization blocked for high-risk object type: {module_name}.{typename}")
            if capability == "restricted" and not allow_restricted:
                raise TypeError(
                    f"Serialization blocked for restricted object type: {module_name}.{typename}")
            # By default, we do not attempt to serialize arbitrary objects
            raise TypeError(
                f"Unsupported type for serialization: {module_name}.{typename}")

        return ser(obj)

    @staticmethod
    def deserialize(obj: Any, allow_restricted: bool = True, allow_high_risk: bool = False) -> Any:
        """Deserialize an object with capability enforcement."""
        def deser(value: Any) -> Any:
            # Primitives pass through
            if value is None or isinstance(value, (bool, int, float, str)):
                return value

            # Tagged structures
            if isinstance(value, dict) and "__type__" in value:
                t = value["__type__"]

                if t == "bytes":
                    b64 = value.get("base64", "")
                    try:
                        return base64.b64decode(b64.encode("ascii"))
                    except Exception as exc:
                        raise ValueError("Invalid base64 for bytes") from exc

                if t == "list":
                    return [deser(v) for v in value.get("items", [])]

                if t == "tuple":
                    return tuple(deser(v) for v in value.get("items", []))

                if t == "set":
                    return set(deser(v) for v in value.get("items", []))

                if t == "dict":
                    items = value.get("items", [])
                    out = {}
                    for pair in items:
                        if not (isinstance(pair, list) or isinstance(pair, tuple)) or len(pair) != 2:
                            raise ValueError(
                                "Invalid dict item in serialized data")
                        k = deser(pair[0])
                        v = deser(pair[1])
                        out[k] = v
                    return out

                if t == "callable":
                    module_name = value.get("module")
                    qualname = value.get("qualname") or value.get("name")
                    capability = SecureSerializer._get_module_capability(
                        module_name)
                    if capability == "restricted" and not allow_restricted:
                        raise ValueError(
                            f"Deserialization blocked: callable from restricted module '{module_name}'")
                    if capability == "high_risk" and not allow_high_risk:
                        raise ValueError(
                            f"Deserialization blocked: callable from high-risk module '{module_name}'")
                    if not module_name or not qualname:
                        raise ValueError(
                            "Invalid callable descriptor during deserialization")

                    mod = importlib.import_module(module_name)
                    target = mod
                    for part in qualname.split("."):
                        if not hasattr(target, part):
                            # Fallback to direct attribute from module if qualname traversal fails
                            target = getattr(mod, value.get("name", qualname))
                            break
                        target = getattr(target, part)

                    if not callable(target):
                        raise ValueError(
                            "Deserialized callable reference is not callable")
                    if not SecureSerializer._is_safe_callable(target):
                        raise ValueError(
                            "Deserialized callable failed safety check")
                    return target

                raise ValueError(f"Unknown serialized type tag: {t}")

            # If it wasn't produced by our serializer but is a container, attempt best-effort walk
            if isinstance(value, list):
                return [deser(v) for v in value]
            if isinstance(value, tuple):
                return tuple(deser(v) for v in value)
            if isinstance(value, set):
                return set(deser(v) for v in value)
            if isinstance(value, dict):
                # Avoid accidentally evaluating unknown schemas; shallow walk
                return {deser(k): deser(v) for k, v in value.items()}

            # Anything else: return as-is (likely already a primitive-compatible type)
            return value

        return deser(obj)
