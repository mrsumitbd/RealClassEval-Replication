from __future__ import annotations

import base64
import datetime as _dt
import importlib
import inspect
import types
import uuid as _uuid
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    _SAFE_MODULES = {
        "builtins",
        "math",
        "operator",
        "functools",
        "itertools",
        "json",
        "statistics",
        "re",
        "decimal",
        "fractions",
        "uuid",
    }
    _RESTRICTED_MODULES = {
        "datetime",
        "time",
        "collections",
        "collections.abc",
        "random",
    }
    _HIGH_RISK_MODULES = {
        "os",
        "sys",
        "subprocess",
        "pathlib",
        "shutil",
        "socket",
        "ctypes",
        "multiprocessing",
        "asyncio",
        "importlib",
        "inspect",
    }

    _TYPE_MARKER = "__serialized__"

    @staticmethod
    def _get_module_capability(module_name):
        """Get the capability level for a module."""
        if not module_name:
            return "unknown"
        top = module_name.split(".", 1)[0]
        if module_name in SecureSerializer._SAFE_MODULES or top in SecureSerializer._SAFE_MODULES:
            return "safe"
        if module_name in SecureSerializer._RESTRICTED_MODULES or top in SecureSerializer._RESTRICTED_MODULES:
            return "restricted"
        if module_name in SecureSerializer._HIGH_RISK_MODULES or top in SecureSerializer._HIGH_RISK_MODULES:
            return "high_risk"
        return "restricted"

    @staticmethod
    def _is_safe_callable(obj):
        """Check if a callable is safe to serialize."""
        if not callable(obj):
            return False

        # Disallow bound methods or callables that capture state
        if inspect.ismethod(obj):
            return False

        # Disallow functools.partial and other callables that aren't plain functions or builtins
        if isinstance(obj, (type(lambda: None),)) or inspect.isfunction(obj):
            # Reject lambdas, nested functions, or closures
            if obj.__name__ == "<lambda>":
                return False
            qualname = getattr(obj, "__qualname__", "")
            if "<locals>" in qualname:
                return False
            if getattr(obj, "__closure__", None):
                return False
            module_name = getattr(obj, "__module__", None)
            cap = SecureSerializer._get_module_capability(module_name)
            return cap in {"safe", "restricted"}
        if inspect.isbuiltin(obj):
            module_name = getattr(obj, "__module__", "builtins")
            cap = SecureSerializer._get_module_capability(module_name)
            return cap in {"safe", "restricted"}

        # Anything else (e.g., classes, instances with __call__, partials) is not considered safe
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serialize an object with capability checks."""
        def _cap_allowed(mod_name: str | None) -> bool:
            cap = SecureSerializer._get_module_capability(mod_name or "")
            if cap == "safe":
                return True
            if cap == "restricted":
                return bool(allow_restricted)
            if cap == "high_risk":
                return bool(allow_high_risk)
            return False

        def _ensure_module_allowed(mod_name: str | None, ctx: str):
            if not _cap_allowed(mod_name):
                cap = SecureSerializer._get_module_capability(mod_name or "")
                raise ValueError(
                    f"{ctx} from module '{mod_name}' requires capability '{cap}' which is not allowed.")

        def _ser(x: Any) -> Any:
            # Primitives
            if x is None or isinstance(x, (bool, int, float, str)):
                return x

            # Bytes-like
            if isinstance(x, (bytes, bytearray, memoryview)):
                data = bytes(x)
                return {SecureSerializer._TYPE_MARKER: type(x).__name__.lower(), "data": base64.b64encode(data).decode("ascii")}

            # Complex
            if isinstance(x, complex):
                return {SecureSerializer._TYPE_MARKER: "complex", "real": x.real, "imag": x.imag}

            # Decimal
            if isinstance(x, Decimal):
                return {SecureSerializer._TYPE_MARKER: "decimal", "value": str(x)}

            # Fraction
            if isinstance(x, Fraction):
                return {SecureSerializer._TYPE_MARKER: "fraction", "numerator": x.numerator, "denominator": x.denominator}

            # UUID
            if isinstance(x, _uuid.UUID):
                return {SecureSerializer._TYPE_MARKER: "uuid", "value": str(x)}

            # Datetime related
            if isinstance(x, _dt.datetime):
                return {SecureSerializer._TYPE_MARKER: "datetime", "value": x.isoformat()}
            if isinstance(x, _dt.date):
                return {SecureSerializer._TYPE_MARKER: "date", "value": x.isoformat()}
            if isinstance(x, _dt.time):
                return {SecureSerializer._TYPE_MARKER: "time", "value": x.isoformat()}
            if isinstance(x, _dt.timedelta):
                return {SecureSerializer._TYPE_MARKER: "timedelta", "total_seconds": x.total_seconds()}

            # Path-like
            if isinstance(x, Path):
                _ensure_module_allowed("pathlib", "Path object")
                return {SecureSerializer._TYPE_MARKER: "path", "value": str(x)}

            # Sequences
            if isinstance(x, list):
                return [_ser(i) for i in x]
            if isinstance(x, tuple):
                return {SecureSerializer._TYPE_MARKER: "tuple", "items": [_ser(i) for i in x]}
            if isinstance(x, set):
                return {SecureSerializer._TYPE_MARKER: "set", "items": [_ser(i) for i in x]}
            if isinstance(x, frozenset):
                return {SecureSerializer._TYPE_MARKER: "frozenset", "items": [_ser(i) for i in x]}

            # Callable
            if callable(x):
                if not SecureSerializer._is_safe_callable(x):
                    raise TypeError(
                        "Callable is not considered safe to serialize.")
                mod_name = getattr(x, "__module__", None)
                _ensure_module_allowed(mod_name, "Callable")
                return {SecureSerializer._TYPE_MARKER: "callable", "module": mod_name, "name": getattr(x, "__name__", None)}

            # Mapping
            if isinstance(x, dict):
                # If all keys are strings and marker isn't used for our types, keep as plain dict
                all_str_keys = all(isinstance(k, str) for k in x.keys())
                if all_str_keys:
                    out = {}
                    for k, v in x.items():
                        out[k] = _ser(v)
                    return out
                # Otherwise, encode as item list to preserve key types
                items = [[_ser(k), _ser(v)] for k, v in x.items()]
                return {SecureSerializer._TYPE_MARKER: "dict", "items": items}

            # Fallback: reject unknown objects for safety
            cls = type(x)
            mod_name = getattr(cls, "__module__", None)
            _ensure_module_allowed(mod_name, f"Object of type {cls.__name__}")
            raise TypeError(
                f"Unsupported object type for serialization: {cls.__module__}.{cls.__name__}")

        return _ser(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        """Deserialize an object with capability enforcement."""
        def _cap_allowed(mod_name: str | None) -> bool:
            cap = SecureSerializer._get_module_capability(mod_name or "")
            if cap == "safe":
                return True
            if cap == "restricted":
                return bool(allow_restricted)
            if cap == "high_risk":
                return bool(allow_high_risk)
            return False

        def _ensure_module_allowed(mod_name: str | None, ctx: str):
            if not _cap_allowed(mod_name):
                cap = SecureSerializer._get_module_capability(mod_name or "")
                raise ValueError(
                    f"{ctx} from module '{mod_name}' requires capability '{cap}' which is not allowed.")

        def _deser(x: Any) -> Any:
            # Primitives pass through
            if x is None or isinstance(x, (bool, int, float, str)):
                return x

            # List (generic sequence)
            if isinstance(x, list):
                return [_deser(i) for i in x]

            # Mapping and tagged types
            if isinstance(x, dict):
                marker = x.get(SecureSerializer._TYPE_MARKER, None)
                if marker is None:
                    # Plain dict with string keys
                    out = {}
                    for k, v in x.items():
                        out[k] = _deser(v)
                    return out

                # Tagged types
                if marker == "bytes":
                    return base64.b64decode(x["data"])
                if marker == "bytearray":
                    return bytearray(base64.b64decode(x["data"]))
                if marker == "memoryview":
                    return memoryview(base64.b64decode(x["data"]))

                if marker == "complex":
                    return complex(x["real"], x["imag"])
                if marker == "decimal":
                    return Decimal(x["value"])
                if marker == "fraction":
                    return Fraction(x["numerator"], x["denominator"])
                if marker == "uuid":
                    return _uuid.UUID(x["value"])

                if marker == "datetime":
                    return _dt.datetime.fromisoformat(x["value"])
                if marker == "date":
                    return _dt.date.fromisoformat(x["value"])
                if marker == "time":
                    return _dt.time.fromisoformat(x["value"])
                if marker == "timedelta":
                    return _dt.timedelta(seconds=float(x["total_seconds"]))

                if marker == "path":
                    _ensure_module_allowed("pathlib", "Path object")
                    return Path(x["value"])

                if marker == "tuple":
                    return tuple(_deser(i) for i in x["items"])
                if marker == "set":
                    return set(_deser(i) for i in x["items"])
                if marker == "frozenset":
                    return frozenset(_deser(i) for i in x["items"])
                if marker == "dict":
                    result = {}
                    for k_ser, v_ser in x["items"]:
                        k = _deser(k_ser)
                        v = _deser(v_ser)
                        result[k] = v
                    return result

                if marker == "callable":
                    mod_name = x.get("module")
                    name = x.get("name")
                    _ensure_module_allowed(mod_name, "Callable")
                    if not mod_name or not name:
                        raise ValueError(
                            "Malformed callable serialization payload.")
                    mod = importlib.import_module(mod_name)
                    func = getattr(mod, name, None)
                    if func is None:
                        raise ValueError(
                            f"Callable {name} not found in module {mod_name}.")
                    if not SecureSerializer._is_safe_callable(func):
                        raise TypeError(
                            "Deserialized callable is not considered safe.")
                    return func

                raise TypeError(f"Unknown serialized marker: {marker}")

            # Fallback reject
            raise TypeError(f"Unsupported serialized type: {type(x).__name__}")

        return _deser(obj)
