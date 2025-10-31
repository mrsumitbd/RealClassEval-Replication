
import json
import pickle
import inspect
import importlib
from types import ModuleType, FunctionType, BuiltinFunctionType, MethodType


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        module = importlib.import_module(module_name)
        if hasattr(module, '__all__'):
            return 'restricted'
        elif module_name in ['os', 'sys', 'subprocess', 'ctypes', 'shutil', 'tempfile']:
            return 'high_risk'
        else:
            return 'safe'

    @staticmethod
    def _is_safe_callable(obj):
        if isinstance(obj, (FunctionType, BuiltinFunctionType, MethodType)):
            module = inspect.getmodule(obj)
            if module is None:
                return False
            module_name = module.__name__
            capability = SecureSerializer._get_module_capability(module_name)
            if capability == 'high_risk':
                return False
            elif capability == 'restricted':
                return False
            else:
                return True
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        def default_serializer(obj):
            if isinstance(obj, (FunctionType, BuiltinFunctionType, MethodType)):
                if not SecureSerializer._is_safe_callable(obj):
                    if not allow_high_risk and SecureSerializer._get_module_capability(inspect.getmodule(obj).__name__) == 'high_risk':
                        raise ValueError(
                            f"Serialization of high-risk callable {obj.__name__} is not allowed")
                    if not allow_restricted and SecureSerializer._get_module_capability(inspect.getmodule(obj).__name__) == 'restricted':
                        raise ValueError(
                            f"Serialization of restricted callable {obj.__name__} is not allowed")
                return {'__callable__': obj.__name__, '__module__': inspect.getmodule(obj).__name__}
            elif isinstance(obj, ModuleType):
                if not allow_high_risk and SecureSerializer._get_module_capability(obj.__name__) == 'high_risk':
                    raise ValueError(
                        f"Serialization of high-risk module {obj.__name__} is not allowed")
                if not allow_restricted and SecureSerializer._get_module_capability(obj.__name__) == 'restricted':
                    raise ValueError(
                        f"Serialization of restricted module {obj.__name__} is not allowed")
                return {'__module__': obj.__name__}
            raise TypeError(
                f"Object of type {type(obj).__name__} is not JSON serializable")

        return json.dumps(obj, default=default_serializer)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        def object_hook(obj):
            if '__callable__' in obj and '__module__' in obj:
                module_name = obj['__module__']
                if not allow_high_risk and SecureSerializer._get_module_capability(module_name) == 'high_risk':
                    raise ValueError(
                        f"Deserialization of high-risk callable from module {module_name} is not allowed")
                if not allow_restricted and SecureSerializer._get_module_capability(module_name) == 'restricted':
                    raise ValueError(
                        f"Deserialization of restricted callable from module {module_name} is not allowed")
                module = importlib.import_module(module_name)
                return getattr(module, obj['__callable__'])
            elif '__module__' in obj:
                module_name = obj['__module__']
                if not allow_high_risk and SecureSerializer._get_module_capability(module_name) == 'high_risk':
                    raise ValueError(
                        f"Deserialization of high-risk module {module_name} is not allowed")
                if not allow_restricted and SecureSerializer._get_module_capability(module_name) == 'restricted':
                    raise ValueError(
                        f"Deserialization of restricted module {module_name} is not allowed")
                return importlib.import_module(module_name)
            return obj

        return json.loads(obj, object_hook=object_hook)
