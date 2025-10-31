
import pickle
import types


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        restricted_modules = {'os', 'subprocess', 'shutil'}
        high_risk_modules = {'ctypes', 'multiprocessing'}

        if module_name in restricted_modules:
            return 'restricted'
        elif module_name in high_risk_modules:
            return 'high_risk'
        else:
            return 'safe'

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if the callable object is safe to use.'''
        if isinstance(obj, (types.BuiltinFunctionType, types.BuiltinMethodType)):
            return True
        elif isinstance(obj, types.FunctionType):
            module_name = obj.__module__
            capability = SecureSerializer._get_module_capability(module_name)
            return capability == 'safe'
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        def safe_pickler(obj):
            if isinstance(obj, dict):
                return {k: safe_pickler(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [safe_pickler(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(safe_pickler(item) for item in obj)
            elif isinstance(obj, set):
                return {safe_pickler(item) for item in obj}
            elif callable(obj):
                if SecureSerializer._is_safe_callable(obj):
                    return obj
                elif allow_restricted and SecureSerializer._get_module_capability(obj.__module__) == 'restricted':
                    return obj
                elif allow_high_risk and SecureSerializer._get_module_capability(obj.__module__) == 'high_risk':
                    return obj
                else:
                    raise ValueError(
                        f"Callable from module {obj.__module__} is not allowed.")
            return obj

        safe_obj = safe_pickler(obj)
        return pickle.dumps(safe_obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        loaded_obj = pickle.loads(obj)

        def enforce_capabilities(obj):
            if isinstance(obj, dict):
                return {k: enforce_capabilities(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [enforce_capabilities(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(enforce_capabilities(item) for item in obj)
            elif isinstance(obj, set):
                return {enforce_capabilities(item) for item in obj}
            elif callable(obj):
                module_name = obj.__module__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'safe':
                    return obj
                elif allow_restricted and capability == 'restricted':
                    return obj
                elif allow_high_risk and capability == 'high_risk':
                    return obj
                else:
                    raise ValueError(
                        f"Callable from module {module_name} is not allowed.")
            return obj

        return enforce_capabilities(loaded_obj)
