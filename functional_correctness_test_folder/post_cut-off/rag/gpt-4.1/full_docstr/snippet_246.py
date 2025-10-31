import types
import pickle


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''

    # Example capability levels for demonstration
    _MODULE_CAPABILITIES = {
        'builtins': 'safe',
        'math': 'safe',
        'os': 'restricted',
        'sys': 'restricted',
        'subprocess': 'high_risk',
        'flock': 'safe',
    }

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        return SecureSerializer._MODULE_CAPABILITIES.get(module_name, 'restricted')

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if a callable is safe to serialize.'''
        if not callable(obj):
            return False
        mod = getattr(obj, '__module__', None)
        if mod is None:
            return False
        cap = SecureSerializer._get_module_capability(mod)
        return cap == 'safe'

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        def check(obj):
            if isinstance(obj, types.FunctionType):
                mod = obj.__module__
                cap = SecureSerializer._get_module_capability(mod)
                if cap == 'high_risk' and not allow_high_risk:
                    raise ValueError(
                        f"High risk function from module '{mod}' cannot be serialized.")
                if cap == 'restricted' and not allow_restricted:
                    raise ValueError(
                        f"Restricted function from module '{mod}' cannot be serialized.")
            elif isinstance(obj, (list, tuple, set)):
                for item in obj:
                    check(item)
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    check(k)
                    check(v)
            elif hasattr(obj, '__dict__'):
                for v in vars(obj).values():
                    check(v)
        check(obj)
        return pickle.dumps(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        loaded = pickle.loads(obj)

        def check(obj):
            if isinstance(obj, types.FunctionType):
                mod = obj.__module__
                cap = SecureSerializer._get_module_capability(mod)
                if cap == 'high_risk' and not allow_high_risk:
                    raise ValueError(
                        f"High risk function from module '{mod}' cannot be deserialized.")
                if cap == 'restricted' and not allow_restricted:
                    raise ValueError(
                        f"Restricted function from module '{mod}' cannot be deserialized.")
            elif isinstance(obj, (list, tuple, set)):
                for item in obj:
                    check(item)
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    check(k)
                    check(v)
            elif hasattr(obj, '__dict__'):
                for v in vars(obj).values():
                    check(v)
        check(loaded)
        return loaded
