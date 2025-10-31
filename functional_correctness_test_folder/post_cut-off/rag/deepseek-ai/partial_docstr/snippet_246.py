
import inspect
import pickle
from typing import Any


class SecureSerializer:
    """Security-focused serialization system with capability controls for Flock objects."""

    @staticmethod
    def _get_module_capability(module_name):
        """Get the capability level for a module."""
        if module_name in ('os', 'sys', 'subprocess', 'shutil', 'pickle'):
            return 'high_risk'
        elif module_name in ('json', 'datetime', 'math', 're'):
            return 'restricted'
        else:
            return 'unrestricted'

    @staticmethod
    def _is_safe_callable(obj):
        """Check if a callable is safe to serialize."""
        if not callable(obj):
            return False
        module_name = inspect.getmodule(
            obj).__name__ if inspect.getmodule(obj) else None
        if module_name:
            capability = SecureSerializer._get_module_capability(module_name)
            return capability == 'unrestricted'
        return True

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serialize an object with capability checks."""
        if inspect.ismodule(obj):
            module_name = obj.__name__
            capability = SecureSerializer._get_module_capability(module_name)
            if capability == 'high_risk' and not allow_high_risk:
                raise ValueError(
                    f"Module {module_name} is high-risk and not allowed")
            elif capability == 'restricted' and not allow_restricted:
                raise ValueError(
                    f"Module {module_name} is restricted and not allowed")
        elif callable(obj) and not SecureSerializer._is_safe_callable(obj):
            raise ValueError("Unsafe callable detected")
        return pickle.dumps(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        """Deserialize an object with capability enforcement."""
        deserialized = pickle.loads(obj)
        if inspect.ismodule(deserialized):
            module_name = deserialized.__name__
            capability = SecureSerializer._get_module_capability(module_name)
            if capability == 'high_risk' and not allow_high_risk:
                raise ValueError(
                    f"Module {module_name} is high-risk and not allowed")
            elif capability == 'restricted' and not allow_restricted:
                raise ValueError(
                    f"Module {module_name} is restricted and not allowed")
        elif callable(deserialized) and not SecureSerializer._is_safe_callable(deserialized):
            raise ValueError("Unsafe callable detected")
        return deserialized
