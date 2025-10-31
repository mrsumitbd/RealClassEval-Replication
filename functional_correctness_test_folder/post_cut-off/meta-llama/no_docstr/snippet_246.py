
import dill
import inspect


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        """Returns the capability level of a module."""
        # Define a dictionary to map module names to their respective capability levels
        module_capabilities = {
            'builtins': 'low_risk',
            'math': 'low_risk',
            'statistics': 'low_risk',
            'random': 'restricted',
            'os': 'high_risk',
            'sys': 'high_risk',
            'subprocess': 'high_risk',
            'shutil': 'high_risk',
            '_io': 'high_risk',  # For file operations
        }
        return module_capabilities.get(module_name, 'unknown')

    @staticmethod
    def _is_safe_callable(obj):
        """Checks if an object is a safe callable."""
        if not inspect.isfunction(obj) and not inspect.ismethod(obj):
            return True  # Not a callable

        # Get the module where the object is defined
        module_name = inspect.getmodule(obj).__name__

        capability = SecureSerializer._get_module_capability(module_name)

        if capability == 'high_risk':
            return False
        elif capability == 'restricted':
            return False  # Restricted modules are not allowed by default
        elif capability == 'low_risk' or capability == 'unknown':
            return True  # Low risk or unknown modules are allowed

        return False  # Default to not allowing the callable

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        """Serializes an object using dill.dumps."""
        if not allow_high_risk:
            # Check if the object is a callable and if it's safe
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                if not SecureSerializer._is_safe_callable(obj):
                    raise ValueError(
                        "Serialization of high-risk or restricted callables is not allowed.")

        try:
            return dill.dumps(obj)
        except Exception as e:
            raise ValueError(f"Failed to serialize object: {str(e)}")

    @staticmethod
    def deserialize(obj_bytes, allow_restricted=True, allow_high_risk=False):
        """Deserializes an object using dill.loads."""
        try:
            obj = dill.loads(obj_bytes)
        except Exception as e:
            raise ValueError(f"Failed to deserialize object: {str(e)}")

        if not allow_high_risk:
            # Check if the deserialized object is a callable and if it's safe
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                if not SecureSerializer._is_safe_callable(obj):
                    raise ValueError(
                        "Deserialization of high-risk or restricted callables is not allowed.")

        return obj
