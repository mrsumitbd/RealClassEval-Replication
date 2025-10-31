
from typing import Any
import dill
import inspect


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    @staticmethod
    def _get_module_capability(module_name):
        """Get the capability level for a module."""
        # For demonstration purposes, assume a simple capability mapping
        capability_levels = {
            'safe_module': 'low',
            'restricted_module': 'restricted',
            'high_risk_module': 'high'
        }
        return capability_levels.get(module_name, 'unknown')

    @staticmethod
    def _is_safe_callable(obj):
        """Check if a callable is safe to serialize."""
        if not inspect.isfunction(obj) and not inspect.ismethod(obj):
            return True  # Not a callable, so considered safe
        module_name = inspect.getmodule(obj).__name__
        capability = SecureSerializer._get_module_capability(module_name)
        return capability != 'high'

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serialize an object with capability checks."""
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            if not allow_high_risk and not SecureSerializer._is_safe_callable(obj):
                raise ValueError(
                    "Serialization of high-risk callable is not allowed")
        try:
            return dill.dumps(obj)
        except Exception as e:
            raise ValueError(f"Failed to serialize object: {e}")

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        """Deserialize an object with capability enforcement."""
        try:
            deserialized_obj = dill.loads(obj)
            if inspect.isfunction(deserialized_obj) or inspect.ismethod(deserialized_obj):
                if not allow_high_risk and not SecureSerializer._is_safe_callable(deserialized_obj):
                    raise ValueError(
                        "Deserialization of high-risk callable is not allowed")
            return deserialized_obj
        except Exception as e:
            raise ValueError(f"Failed to deserialize object: {e}")
