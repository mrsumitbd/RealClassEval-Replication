
import json
import importlib
import types
from typing import Any, Dict, List, Tuple, Union

# --------------------------------------------------------------------------- #
#  SecureSerializer – a minimal, capability‑aware (de)serialization helper
# --------------------------------------------------------------------------- #


class SecureSerializer:
    """Security‑focused serialization system with capability controls for Flock objects."""

    # ----------------------------------------------------------------------- #
    #  Capability definitions
    # ----------------------------------------------------------------------- #
    _MODULE_CAPABILITIES: Dict[str, str] = {
        # Safe modules – can be serialized/deserialized without restrictions
        "builtins": "safe",
        "json": "safe",
        "math": "safe",
        "datetime": "safe",
        "collections": "restricted",
        "itertools": "restricted",
        # High‑risk modules – only allowed if explicitly permitted
        "os": "high_risk",
        "subprocess": "high_risk",
        "pickle": "high_risk",
        "importlib": "high_risk",
        "sys": "high_risk",
    }

    @staticmethod
    def _get_module_capability(module_name: str) -> str:
        """
        Return the capability level for a module.

        Parameters
        ----------
        module_name : str
            The name of the module to inspect.

        Returns
        -------
        str
            One of ``'safe'``, ``'restricted'``, ``'high_risk'`` or ``'unsafe'``.
        """
        return SecureSerializer._MODULE_CAPABILITIES.get(module_name, "unsafe")

    @staticmethod
    def _is_safe_callable(obj: Any) -> bool:
        """
        Check if a callable is safe to serialize.

        Parameters
        ----------
        obj : Any
            The object to test.

        Returns
        -------
        bool
            ``True`` if the callable is defined in a safe module, otherwise ``False``.
        """
        if not callable(obj):
            return False
        # For bound methods, get the underlying function
        func = getattr(obj, "__func__", obj)
        module_name = getattr(func, "__module__", None)
        if module_name is None:
            return False
        return SecureSerializer._get_module_capability(module_name) == "safe"

    # ----------------------------------------------------------------------- #
    #  Serialization helpers
    # ----------------------------------------------------------------------- #
    @staticmethod
    def _serialize_obj(obj: Any, allow_restricted: bool, allow_high_risk: bool) -> Any:
        """
        Recursively serialize an object into JSON‑serialisable data.

        Parameters
        ----------
        obj : Any
            The object to serialize.
        allow_restricted : bool
            Whether to allow objects from restricted modules.
        allow_high_risk : bool
            Whether to allow objects from high‑risk modules.

        Returns
        -------
        Any
            A JSON‑serialisable representation of ``obj``.
        """
        # Basic types are already serialisable
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj

        # Containers – recurse
        if isinstance(obj, (list, tuple)):
            return [SecureSerializer._serialize_obj(v, allow_restricted, allow_high_risk) for v in obj]
        if isinstance(obj, dict):
            return {k: SecureSerializer._serialize_obj(v, allow_restricted, allow_high_risk) for k, v in obj.items()}

        # Functions / callables – only safe ones
        if callable(obj):
            if not SecureSerializer._is_safe_callable(obj):
                raise ValueError(
                    f"Attempted to serialize unsafe callable: {obj!r}")
            # Represent callables by their fully‑qualified name
            return {
                "__callable__": True,
                "module": obj.__module__,
                "name": obj.__qualname__,
            }

        # Custom objects – inspect module capability
        module_name = getattr(obj, "__module__", None)
        if module_name is None:
            raise ValueError(f"Cannot determine module for object: {obj!r}")

        capability = SecureSerializer._get_module_capability(module_name)
        if capability == "unsafe":
            raise ValueError(
                f"Module {module_name!r} is unsafe for serialization.")
        if capability == "restricted" and not allow_restricted:
            raise ValueError(
                f"Module {module_name!r} is restricted and not allowed.")
        if capability == "high_risk" and not allow_high_risk:
            raise ValueError(
                f"Module {module_name!r} is high‑risk and not allowed.")

        # Serialize the object's state
        state = getattr(obj, "__dict__", None)
        if state is None:
            raise ValueError(
                f"Object of type {type(obj).__name__} has no __dict__ and cannot be serialized.")
        return {
            "__class__": type(obj).__name__,
            "__module__": module_name,
            "state": SecureSerializer._serialize_obj(state, allow_restricted, allow_high_risk),
        }

    @staticmethod
    def serialize(obj: Any, allow_restricted: bool = True, allow_high_risk: bool = False) -> str:
        """
        Serialize an object with capability checks.

        Parameters
        ----------
        obj : Any
            The object to serialize.
        allow_restricted : bool, optional
            Whether to allow objects from restricted modules.
        allow_high_risk : bool, optional
            Whether to allow objects from high‑risk modules.

        Returns
        -------
        str
            A JSON string representing the serialized object.
        """
        serialised = SecureSerializer._serialize_obj(
            obj, allow_restricted, allow_high_risk)
        return json.dumps(serialised)

    # ----------------------------------------------------------------------- #
    #  Deserialization helpers
    # ----------------------------------------------------------------------- #
    @staticmethod
    def _deserialize_obj(data: Any, allow_restricted: bool, allow_high_risk: bool) -> Any:
        """
        Recursively deserialize JSON data into Python objects.

        Parameters
        ----------
        data : Any
            The JSON data to deserialize.
        allow_restricted : bool
            Whether to allow objects from restricted modules.
        allow_high_risk : bool
            Whether to allow objects from high‑risk modules.

        Returns
        -------
        Any
            The reconstructed Python object.
        """
        # Basic types
        if data is None or isinstance(data, (bool, int, float, str)):
            return data

        # Containers
        if isinstance(data, list):
            return [SecureSerializer._deserialize_obj(v, allow_restricted, allow_high_risk) for v in data]
        if isinstance(data, dict):
            # Detect special markers
            if "__callable__" in data:
                module_name = data["module"]
                name = data["name"]
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == "unsafe":
                    raise ValueError(
                        f"Module {module_name!r} is unsafe for deserialization.")
                if capability == "restricted" and not allow_restricted:
                    raise ValueError(
                        f"Module {module_name!r} is restricted and not allowed.")
                if capability == "high_risk" and not allow
