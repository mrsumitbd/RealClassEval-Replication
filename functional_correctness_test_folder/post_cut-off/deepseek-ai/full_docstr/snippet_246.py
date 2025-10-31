
import pickle
import inspect
import types


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''
    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        restricted_modules = {'os', 'sys', 'subprocess', 'shutil'}
        high_risk_modules = {'ctypes', 'socket', 'pickle', 'marshal'}

        if module_name in restricted_modules:
            return 'restricted'
        elif module_name in high_risk_modules:
            return 'high_risk'
        else:
            return 'low_risk'

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if a callable is safe to serialize.'''
        if not callable(obj):
            return False

        if isinstance(obj, types.BuiltinFunctionType):
            module_name = obj.__module__
            capability = SecureSerializer._get_module_capability(module_name)
            return capability == 'low_risk'

        if isinstance(obj, (types.FunctionType, types.MethodType)):
            try:
                module_name = inspect.getmodule(obj).__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                return capability == 'low_risk'
            except:
                return False

        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        if isinstance(obj, type):
            raise ValueError("Cannot serialize class objects.")

        if callable(obj):
            if not SecureSerializer._is_safe_callable(obj):
                raise ValueError("Unsafe callable detected.")

        try:
            return pickle.dumps(obj)
        except (pickle.PicklingError, TypeError) as e:
            raise ValueError(f"Serialization failed: {e}")

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        try:
            deserialized = pickle.loads(obj)

            if callable(deserialized):
                if not SecureSerializer._is_safe_callable(deserialized):
                    raise ValueError(
                        "Unsafe callable detected in deserialized object.")

            return deserialized
        except (pickle.UnpicklingError, TypeError) as e:
            raise ValueError(f"Deserialization failed: {e}")
