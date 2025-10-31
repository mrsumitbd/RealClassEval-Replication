
import pickle
import inspect
import types


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        restricted_modules = {
            'os': 'high_risk',
            'subprocess': 'high_risk',
            'sys': 'restricted',
            'pickle': 'restricted',
        }
        return restricted_modules.get(module_name, 'safe')

    @staticmethod
    def _is_safe_callable(obj):
        if not callable(obj):
            return False

        if isinstance(obj, (types.BuiltinFunctionType, types.BuiltinMethodType)):
            module_name = obj.__module__
            capability = SecureSerializer._get_module_capability(module_name)
            return capability == 'safe'

        if isinstance(obj, (types.FunctionType, types.MethodType)):
            module_name = inspect.getmodule(
                obj).__name__ if inspect.getmodule(obj) else None
            if module_name:
                capability = SecureSerializer._get_module_capability(
                    module_name)
                return capability == 'safe'
            return True  # Assume safe if no module (e.g., locally defined)

        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        if isinstance(obj, (int, float, str, bool, list, tuple, dict, set, bytes)):
            return pickle.dumps(obj)

        if callable(obj):
            if not SecureSerializer._is_safe_callable(obj):
                if not allow_restricted and not allow_high_risk:
                    raise ValueError("Unsafe callable detected")
                module_name = getattr(inspect.getmodule(obj), '__name__', None)
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'high_risk' and not allow_high_risk:
                    raise ValueError("High-risk callable not allowed")
                if capability == 'restricted' and not allow_restricted:
                    raise ValueError("Restricted callable not allowed")
            return pickle.dumps(obj)

        raise ValueError("Unsupported object type for serialization")

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        deserialized = pickle.loads(obj)

        if callable(deserialized):
            if not SecureSerializer._is_safe_callable(deserialized):
                module_name = getattr(inspect.getmodule(
                    deserialized), '__name__', None)
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'high_risk' and not allow_high_risk:
                    raise ValueError("High-risk callable not allowed")
                if capability == 'restricted' and not allow_restricted:
                    raise ValueError("Restricted callable not allowed")

        return deserialized
