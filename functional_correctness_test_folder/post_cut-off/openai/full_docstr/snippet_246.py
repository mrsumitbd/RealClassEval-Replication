
import json
import pickle
import types
import sys
from typing import Any, Dict, Tuple


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''

    # Mapping of module names to capability levels
    _MODULE_CAPABILITIES: Dict[str, str] = {
        'builtins': 'public',
        'json': 'public',
        'pickle': 'public',
        'types': 'public',
        'sys': 'public',
        'os': 'restricted',
        'subprocess': 'high_risk',
        'flock': 'public',  # example custom module
    }

    @staticmethod
    def _get_module_capability(module_name: str) -> str:
        '''Get the capability level for a module.'''
        return SecureSerializer._MODULE_CAPABILITIES.get(module_name, 'public')

    @staticmethod
    def _is_safe_callable(obj: Any) -> bool:
        '''Check if a callable is safe to serialize.'''
        if not callable(obj):
            return False
        # Functions and methods have __module__ attribute
        module_name = getattr(obj, '__module__', None)
        if module_name is None:
            return False
        capability = SecureSerializer._get_module_capability(module_name)
        return capability == 'public'

    @staticmethod
    def serialize(
        obj: Any,
        allow_restricted: bool = True,
        allow_high_risk: bool = False
    ) -> Any:
        '''Serialize an object with capability checks.'''
        # Helper to decide if a module is allowed
        def module_allowed(module_name: str) -> bool:
            cap = SecureSerializer._get_module_capability(module_name)
            if cap == 'high_risk' and not allow_high_risk:
                return False
            if cap == 'restricted' and not allow_restricted:
                return False
            return True

        # Simple types can be JSON-encoded
        if isinstance(obj, (int, float, str, bool, type(None))):
            return json.dumps(obj)

        if isinstance(obj, (list, tuple, set)):
            # Serialize each element recursively
            return json.dumps([SecureSerializer.serialize(item, allow_restricted, allow_high_risk) for item in obj])

        if isinstance(obj, dict):
            # Serialize keys and values recursively
            return json.dumps({
                SecureSerializer.serialize(k, allow_restricted, allow_high_risk): SecureSerializer.serialize(v, allow_restricted, allow_high_risk)
                for k, v in obj.items()
            })

        # For callables, ensure they are safe
        if callable(obj):
            if not SecureSerializer._is_safe_callable(obj):
                raise ValueError(f"Callable {obj} is not safe to serialize.")
            # Serialize the function name and module
            return json.dumps({
                '__callable__': True,
                'module': obj.__module__,
                'name': obj.__qualname__
            })

        # For other objects, use pickle but check module capability
        module_name = getattr(obj, '__module__', None)
        if module_name and not module_allowed(module_name):
            raise ValueError(
                f"Object from module '{module_name}' is not allowed for serialization.")

        try:
            return pickle.dumps(obj)
        except Exception as e:
            raise ValueError(f"Failed to pickle object: {e}") from e

    @staticmethod
    def deserialize(
        data: Any,
        allow_restricted: bool = True,
        allow_high_risk: bool = False
    ) -> Any:
        '''Deserialize an object with capability enforcement.'''
        # Helper to decide if a module is allowed
        def module_allowed(module_name: str) -> bool:
            cap = SecureSerializer._get_module_capability(module_name)
            if cap == 'high_risk' and not allow_high_risk:
                return False
            if cap == 'restricted' and not allow_restricted:
                return False
            return True

        # If data is a JSON string, attempt to parse
        if isinstance(data, str):
            try:
                obj = json.loads(data)
            except json.JSONDecodeError:
                # Not JSON, try pickle
                try:
                    obj = pickle.loads(data.encode('latin1'))
                except Exception:
                    raise ValueError("Data is neither valid JSON nor pickle.")
                else:
                    # After unpickling, check module capability
                    module_name = getattr(obj, '__module__', None)
                    if module_name and not module_allowed(module_name):
                        raise ValueError(
                            f"Deserialized object from module '{module_name}' is not allowed.")
                    return obj

            # If JSON dict with __callable__ flag
            if isinstance(obj, dict) and obj.get('__callable__'):
                module_name = obj.get('module')
                name = obj.get('name')
                if not module_allowed(module_name):
                    raise ValueError(
                        f"Callable from module '{module_name}' is not allowed.")
                try:
                    mod = __import__(module_name, fromlist=[name])
                    func = getattr(mod, name)
                except Exception as e:
                    raise ValueError(
                        f"Failed to import callable {name} from {module_name}: {e}") from e
                return func

            # For other JSON types, return as is
            return obj

        # If data is bytes, try pickle
        if isinstance(data, (bytes, bytearray)):
            try:
                obj = pickle.loads(data)
            except Exception as e:
                raise ValueError(f"Failed to unpickle data: {e}") from e
            module_name = getattr(obj, '__module__', None)
            if module_name and not module_allowed(module_name):
                raise ValueError(
                    f"Deserialized object from module '{module_name}' is not allowed.")
            return obj

        # Unsupported data type
        raise TypeError(
            f"Unsupported data type for deserialization: {type(data)}")
