
import io
import pickle
import types


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''

    # Capability levels
    _CAPABILITY_LEVELS = {
        'builtins': 0,
        'math': 0,
        'random': 1,
        'os': 2,
        'sys': 2,
        'subprocess': 3,
        'socket': 3,
        'flock': 1,  # Example: custom module
    }

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        return SecureSerializer._CAPABILITY_LEVELS.get(module_name, 2)

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if a callable is safe to serialize.'''
        # Only allow functions defined at the top level of safe modules
        if isinstance(obj, types.BuiltinFunctionType):
            return True
        if isinstance(obj, types.FunctionType):
            mod = getattr(obj, '__module__', None)
            if mod is None:
                return False
            cap = SecureSerializer._get_module_capability(mod)
            return cap <= 1
        if isinstance(obj, types.MethodType):
            # Only allow methods of built-in types
            if isinstance(obj.__self__, type):
                return obj.__self__.__module__ == 'builtins'
            return False
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        # Recursively check for callables and their modules
        def check_obj(o):
            if callable(o):
                if not SecureSerializer._is_safe_callable(o):
                    raise ValueError(
                        "Unsafe callable detected during serialization: %r" % o)
            elif isinstance(o, (list, tuple, set)):
                for item in o:
                    check_obj(item)
            elif isinstance(o, dict):
                for k, v in o.items():
                    check_obj(k)
                    check_obj(v)
            elif hasattr(o, '__dict__'):
                for v in vars(o).values():
                    check_obj(v)
        check_obj(obj)
        return pickle.dumps(obj, protocol=4)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        # Custom Unpickler to restrict module loading
        class RestrictedUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                cap = SecureSerializer._get_module_capability(module)
                if cap == 0:
                    return super().find_class(module, name)
                elif cap == 1 and allow_restricted:
                    return super().find_class(module, name)
                elif cap == 2 and allow_high_risk:
                    return super().find_class(module, name)
                else:
                    raise pickle.UnpicklingError(
                        f"Deserialization of {module}.{name} is not allowed (capability {cap})"
                    )
        return RestrictedUnpickler(io.BytesIO(obj)).load()
