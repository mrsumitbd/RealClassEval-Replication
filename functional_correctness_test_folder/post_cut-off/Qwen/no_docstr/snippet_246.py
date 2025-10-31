
import pickle
import importlib
import types


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        try:
            module = importlib.import_module(module_name)
            return getattr(module, 'CAPABILITY', None)
        except ImportError:
            return None

    @staticmethod
    def _is_safe_callable(obj):
        if isinstance(obj, (types.BuiltinFunctionType, types.BuiltinMethodType)):
            return True
        if isinstance(obj, types.FunctionType) and obj.__module__ in ['__main__', 'builtins']:
            return True
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        if not allow_high_risk:
            if isinstance(obj, (types.FunctionType, types.MethodType, types.LambdaType)):
                raise ValueError(
                    "Serialization of functions and methods is not allowed.")
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        if not allow_high_risk:
            raise ValueError(
                "Deserialization is not allowed due to high risk.")
        return pickle.loads(obj)
