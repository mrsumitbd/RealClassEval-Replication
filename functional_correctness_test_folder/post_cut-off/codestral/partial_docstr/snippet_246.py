
import pickle
import inspect
import types
import importlib


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, '__capability__'):
                return module.__capability__
            else:
                return 'low'
        except ImportError:
            return 'low'

    @staticmethod
    def _is_safe_callable(obj):
        if not callable(obj):
            return False

        try:
            module_name = obj.__module__
            capability = SecureSerializer._get_module_capability(module_name)
            if capability == 'high':
                return False
            elif capability == 'restricted':
                return False
            else:
                return True
        except AttributeError:
            return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        def check_obj(o):
            if isinstance(o, (int, float, str, bool, type(None))):
                return True
            elif isinstance(o, (list, tuple, set, frozenset)):
                return all(check_obj(item) for item in o)
            elif isinstance(o, dict):
                return all(check_obj(k) and check_obj(v) for k, v in o.items())
            elif isinstance(o, types.FunctionType):
                if not SecureSerializer._is_safe_callable(o):
                    return False
                return True
            elif isinstance(o, type):
                module_name = o.__module__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'high' and not allow_high_risk:
                    return False
                elif capability == 'restricted' and not allow_restricted:
                    return False
                return True
            else:
                return False

        if not check_obj(obj):
            raise ValueError(
                "Object contains unsafe elements for serialization.")

        return pickle.dumps(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        def enforce_capability(o):
            if isinstance(o, (int, float, str, bool, type(None))):
                return o
            elif isinstance(o, (list, tuple, set, frozenset)):
                return type(o)(enforce_capability(item) for item in o)
            elif isinstance(o, dict):
                return {enforce_capability(k): enforce_capability(v) for k, v in o.items()}
            elif isinstance(o, types.FunctionType):
                if not SecureSerializer._is_safe_callable(o):
                    raise ValueError(
                        "Unsafe function detected during deserialization.")
                return o
            elif isinstance(o, type):
                module_name = o.__module__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'high' and not allow_high_risk:
                    raise ValueError(
                        "High-risk type detected during deserialization.")
                elif capability == 'restricted' and not allow_restricted:
                    raise ValueError(
                        "Restricted type detected during deserialization.")
                return o
            else:
                raise ValueError(
                    "Unsupported type detected during deserialization.")

        try:
            deserialized_obj = pickle.loads(obj)
            return enforce_capability(deserialized_obj)
        except (pickle.PickleError, ValueError) as e:
            raise ValueError(
                "Deserialization failed due to security constraints.") from e
