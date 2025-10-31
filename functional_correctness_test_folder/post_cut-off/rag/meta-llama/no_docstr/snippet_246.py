
import dill
import inspect
from typing import Any


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    @staticmethod
    def _get_module_capability(module_name: str) -> str:
        """Get the capability level for a module."""
        # For demonstration purposes, assume a simple capability mapping
        capability_levels = {
            'safe_module': 'low',
            'restricted_module': 'restricted',
            'high_risk_module': 'high'
        }
        return capability_levels.get(module_name, 'unknown')

    @staticmethod
    def _is_safe_callable(obj: Any) -> bool:
        """Check if a callable is safe to serialize."""
        if not callable(obj):
            return True  # Non-callables are considered safe

        # Check if the object is a lambda function or has a restricted module
        if obj.__name__ == '<lambda>':
            return False

        module_name = inspect.getmodule(obj).__name__
        capability = SecureSerializer._get_module_capability(module_name)
        return capability != 'high'

    @staticmethod
    def serialize(obj: Any, allow_restricted: bool = True, allow_high_risk: bool = False) -> bytes:
        """Serialize an object with capability checks."""
        if not allow_restricted or not allow_high_risk:
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                if not SecureSerializer._is_safe_callable(obj):
                    if not allow_restricted and SecureSerializer._get_module_capability(inspect.getmodule(obj).__name__) == 'restricted':
                        raise ValueError(
                            "Serialization of restricted callables is not allowed")
                    elif not allow_high_risk and SecureSerializer._get_module_capability(inspect.getmodule(obj).__name__) == 'high':
                        raise ValueError(
                            "Serialization of high-risk callables is not allowed")

        return dill.dumps(obj)

    @staticmethod
    def deserialize(obj: bytes, allow_restricted: bool = True, allow_high_risk: bool = False) -> Any:
        """Deserialize an object with capability enforcement."""
        deserialized_obj = dill.loads(obj)

        if not allow_restricted or not allow_high_risk:
            if inspect.isfunction(deserialized_obj) or inspect.ismethod(deserialized_obj):
                if not SecureSerializer._is_safe_callable(deserialized_obj):
                    if not allow_restricted and SecureSerializer._get_module_capability(inspect.getmodule(deserialized_obj).__name__) == 'restricted':
                        raise ValueError(
                            "Deserialization of restricted callables is not allowed")
                    elif not allow_high_risk and SecureSerializer._get_module_capability(inspect.getmodule(deserialized_obj).__name__) == 'high':
                        raise ValueError(
                            "Deserialization of high-risk callables is not allowed")

        return deserialized_obj
