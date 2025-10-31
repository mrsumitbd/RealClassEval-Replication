
import dill
import inspect
import importlib


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''
    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        # For demonstration purposes, we'll use a simple capability mapping.
        # In a real application, this could be a more complex function or a database lookup.
        capability_levels = {
            'builtins': 'low_risk',
            'math': 'low_risk',
            'random': 'restricted',
            'os': 'high_risk',
            'sys': 'high_risk',
            'subprocess': 'high_risk',
        }
        return capability_levels.get(module_name, 'unknown')

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if a callable is safe to serialize.'''
        if not inspect.isfunction(obj) and not inspect.ismethod(obj):
            return True  # Not a callable, so it's considered safe.

        module_name = inspect.getmodule(obj).__name__
        capability = SecureSerializer._get_module_capability(module_name)

        if capability == 'high_risk':
            return False
        elif capability == 'restricted':
            # For restricted modules, we allow serialization but with a warning.
            print(
                f"Warning: Serializing a callable from a restricted module: {module_name}")
            return True
        else:
            return True

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        try:
            # Check if the object contains any callables that are not safe to serialize.
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                if not SecureSerializer._is_safe_callable(obj):
                    if not allow_high_risk:
                        raise ValueError(
                            "Serialization of high-risk callables is not allowed.")
            else:
                # Recursively check the object's contents for unsafe callables.
                for item in obj.__dict__.values() if hasattr(obj, '__dict__') else []:
                    if inspect.isfunction(item) or inspect.ismethod(item):
                        if not SecureSerializer._is_safe_callable(item):
                            if not allow_high_risk:
                                raise ValueError(
                                    "Serialization of high-risk callables is not allowed.")
                    elif isinstance(item, (list, tuple)):
                        for subitem in item:
                            if inspect.isfunction(subitem) or inspect.ismethod(subitem):
                                if not SecureSerializer._is_safe_callable(subitem):
                                    if not allow_high_risk:
                                        raise ValueError(
                                            "Serialization of high-risk callables is not allowed.")

            # If we've reached this point, it's safe to serialize the object.
            return dill.dumps(obj)
        except Exception as e:
            raise ValueError(f"Failed to serialize object: {str(e)}")

    @staticmethod
    def deserialize(obj_bytes, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        try:
            obj = dill.loads(obj_bytes)

            # Check if the deserialized object contains any callables that are not safe.
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                if not SecureSerializer._is_safe_callable(obj):
                    if not allow_high_risk:
                        raise ValueError(
                            "Deserialization of high-risk callables is not allowed.")
            else:
                # Recursively check the object's contents for unsafe callables.
                for item in obj.__dict__.values() if hasattr(obj, '__dict__') else []:
                    if inspect.isfunction(item) or inspect.ismethod(item):
                        if not SecureSerializer._is_safe_callable(item):
                            if not allow_high_risk:
                                raise ValueError(
                                    "Deserialization of high-risk callables is not allowed.")
                    elif isinstance(item, (list, tuple)):
                        for subitem in item:
                            if inspect.isfunction(subitem) or inspect.ismethod(subitem):
                                if not SecureSerializer._is_safe_callable(subitem):
                                    if not allow_high_risk:
                                        raise ValueError(
                                            "Deserialization of high-risk callables is not allowed.")

            return obj
        except Exception as e:
            raise ValueError(f"Failed to deserialize object: {str(e)}")


# Example usage:
if __name__ == "__main__":
    def test_func():
        return "Hello, World!"

    serialized = SecureSerializer.serialize(test_func)
    deserialized = SecureSerializer.deserialize(serialized)

    print(deserialized())  # Output: Hello, World!
