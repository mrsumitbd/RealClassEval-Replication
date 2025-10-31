
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
        return capability in ['low']

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serialize an object with capability checks."""
        if not allow_restricted or not allow_high_risk:
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                module_name = inspect.getmodule(obj).__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'restricted' and not allow_restricted:
                    raise ValueError(
                        f"Serialization of restricted module {module_name} is not allowed")
                if capability == 'high' and not allow_high_risk:
                    raise ValueError(
                        f"Serialization of high-risk module {module_name} is not allowed")
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if inspect.isfunction(v) or inspect.ismethod(v):
                        if not SecureSerializer._is_safe_callable(v):
                            module_name = inspect.getmodule(v).__name__
                            capability = SecureSerializer._get_module_capability(
                                module_name)
                            if capability == 'restricted' and not allow_restricted:
                                raise ValueError(
                                    f"Serialization of restricted module {module_name} is not allowed")
                            if capability == 'high' and not allow_high_risk:
                                raise ValueError(
                                    f"Serialization of high-risk module {module_name} is not allowed")
        return dill.dumps(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        """Deserialize an object with capability enforcement."""
        deserialized_obj = dill.loads(obj)
        if not allow_restricted or not allow_high_risk:
            if inspect.isfunction(deserialized_obj) or inspect.ismethod(deserialized_obj):
                if not SecureSerializer._is_safe_callable(deserialized_obj):
                    module_name = inspect.getmodule(deserialized_obj).__name__
                    capability = SecureSerializer._get_module_capability(
                        module_name)
                    if capability == 'restricted' and not allow_restricted:
                        raise ValueError(
                            f"Deserialization of restricted module {module_name} is not allowed")
                    if capability == 'high' and not allow_high_risk:
                        raise ValueError(
                            f"Deserialization of high-risk module {module_name} is not allowed")
            elif isinstance(deserialized_obj, dict):
                for k, v in deserialized_obj.items():
                    if inspect.isfunction(v) or inspect.ismethod(v):
                        if not SecureSerializer._is_safe_callable(v):
                            module_name = inspect.getmodule(v).__name__
                            capability = SecureSerializer._get_module_capability(
                                module_name)
                            if capability == 'restricted' and not allow_restricted:
                                raise ValueError(
                                    f"Deserialization of restricted module {module_name} is not allowed")
                            if capability == 'high' and not allow_high_risk:
                                raise ValueError(
                                    f"Deserialization of high-risk module {module_name} is not allowed")
        return deserialized_obj
