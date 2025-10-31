
import inspect
from typing import Any


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    @staticmethod
    def _get_module_capability(module_name):
        """Get the capability level for a module."""
        # Default implementation - can be overridden or extended
        if module_name in ('os', 'sys', 'subprocess'):
            return 'high_risk'
        elif module_name in ('json', 'pickle', 'datetime'):
            return 'restricted'
        else:
            return 'safe'

    @staticmethod
    def _is_safe_callable(obj):
        """Check if a callable is safe to serialize."""
        if not callable(obj):
            return False

        module = inspect.getmodule(obj)
        if module is None:
            return False

        module_name = module.__name__
        capability = SecureSerializer._get_module_capability(module_name)

        return capability == 'safe'

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serialize an object with capability checks."""
        if callable(obj) and not SecureSerializer._is_safe_callable(obj):
            raise ValueError("Unsafe callable detected in serialization")

        # Default serialization logic (placeholder)
        try:
            import pickle
            return pickle.dumps(obj)
        except Exception as e:
            raise ValueError(f"Serialization failed: {str(e)}")

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        """Deserialize an object with capability enforcement."""
        try:
            import pickle
            deserialized = pickle.loads(obj)

            if callable(deserialized) and not SecureSerializer._is_safe_callable(deserialized):
                raise ValueError(
                    "Unsafe callable detected in deserialized object")

            return deserialized
        except Exception as e:
            raise ValueError(f"Deserialization failed: {str(e)}")
