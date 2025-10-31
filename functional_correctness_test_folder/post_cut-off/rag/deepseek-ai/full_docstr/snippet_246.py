
import inspect
import pickle
from typing import Any


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    @staticmethod
    def _get_module_capability(module_name):
        """Get the capability level for a module."""
        # Example implementation: check a predefined capability mapping
        capability_map = {
            'builtins': 'low',
            'os': 'high',
            'sys': 'high',
            'json': 'low',
            'pickle': 'restricted'
        }
        return capability_map.get(module_name, 'unknown')

    @staticmethod
    def _is_safe_callable(obj):
        """Check if a callable is safe to serialize."""
        if not callable(obj):
            return False

        # Check if the callable is a built-in or from a safe module
        module = inspect.getmodule(obj)
        if module is None:
            return True  # Assume built-in or safe if no module

        module_name = module.__name__
        capability = SecureSerializer._get_module_capability(module_name)

        return capability in ('low', 'unknown')

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serialize an object with capability checks."""
        if inspect.ismodule(obj):
            raise ValueError("Cannot serialize modules directly.")

        if callable(obj) and not SecureSerializer._is_safe_callable(obj):
            raise ValueError("Unsafe callable detected.")

        # Additional checks for restricted/high-risk objects
        module = inspect.getmodule(obj)
        if module is not None:
            module_name = module.__name__
            capability = SecureSerializer._get_module_capability(module_name)
            if capability == 'restricted' and not allow_restricted:
                raise ValueError("Restricted module access not allowed.")
            if capability == 'high' and not allow_high_risk:
                raise ValueError("High-risk module access not allowed.")

        return pickle.dumps(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        """Deserialize an object with capability enforcement."""
        deserialized = pickle.loads(obj)

        # Post-deserialization checks
        if inspect.ismodule(deserialized):
            raise ValueError("Deserialized object cannot be a module.")

        if callable(deserialized) and not SecureSerializer._is_safe_callable(deserialized):
            raise ValueError(
                "Unsafe callable detected in deserialized object.")

        module = inspect.getmodule(deserialized)
        if module is not None:
            module_name = module.__name__
            capability = SecureSerializer._get_module_capability(module_name)
            if capability == 'restricted' and not allow_restricted:
                raise ValueError("Restricted module access not allowed.")
            if capability == 'high' and not allow_high_risk:
                raise ValueError("High-risk module access not allowed.")

        return deserialized
