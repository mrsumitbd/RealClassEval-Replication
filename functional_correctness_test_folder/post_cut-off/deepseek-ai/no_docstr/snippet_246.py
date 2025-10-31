
import inspect
import types
import builtins
import importlib


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        restricted_modules = {
            'os': 'high_risk',
            'subprocess': 'high_risk',
            'sys': 'restricted',
            'pickle': 'restricted',
            'marshal': 'high_risk',
            'ctypes': 'high_risk',
            'socket': 'high_risk'
        }
        return restricted_modules.get(module_name, 'safe')

    @staticmethod
    def _is_safe_callable(obj):
        if not callable(obj):
            return False

        if isinstance(obj, (types.BuiltinFunctionType, types.BuiltinMethodType)):
            return False

        if isinstance(obj, (types.FunctionType, types.MethodType, types.LambdaType)):
            module_name = obj.__module__
            if module_name == 'builtins':
                return False
            capability = SecureSerializer._get_module_capability(module_name)
            return capability == 'safe'

        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        if isinstance(obj, (int, float, str, bool, bytes, type(None))):
            return obj
        elif isinstance(obj, (list, tuple, set)):
            return [SecureSerializer.serialize(item, allow_restricted, allow_high_risk) for item in obj]
        elif isinstance(obj, dict):
            return {SecureSerializer.serialize(k, allow_restricted, allow_high_risk):
                    SecureSerializer.serialize(
                        v, allow_restricted, allow_high_risk)
                    for k, v in obj.items()}
        elif hasattr(obj, '__dict__'):
            return {
                '__class__': obj.__class__.__name__,
                '__module__': obj.__module__,
                'data': SecureSerializer.serialize(obj.__dict__, allow_restricted, allow_high_risk)
            }
        else:
            capability = SecureSerializer._get_module_capability(
                obj.__module__)
            if capability == 'high_risk' and not allow_high_risk:
                raise ValueError(
                    f"Serialization of high-risk module {obj.__module__} is not allowed")
            if capability == 'restricted' and not allow_restricted:
                raise ValueError(
                    f"Serialization of restricted module {obj.__module__} is not allowed")
            return obj

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        if isinstance(obj, (int, float, str, bool, bytes, type(None))):
            return obj
        elif isinstance(obj, list):
            return [SecureSerializer.deserialize(item, allow_restricted, allow_high_risk) for item in obj]
        elif isinstance(obj, dict):
            if '__class__' in obj and '__module__' in obj and 'data' in obj:
                module_name = obj['__module__']
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'high_risk' and not allow_high_risk:
                    raise ValueError(
                        f"Deserialization of high-risk module {module_name} is not allowed")
                if capability == 'restricted' and not allow_restricted:
                    raise ValueError(
                        f"Deserialization of restricted module {module_name} is not allowed")

                module = importlib.import_module(module_name)
                cls = getattr(module, obj['__class__'])
                instance = cls.__new__(cls)
                instance.__dict__ = SecureSerializer.deserialize(
                    obj['data'], allow_restricted, allow_high_risk)
                return instance
            else:
                return {SecureSerializer.deserialize(k, allow_restricted, allow_high_risk):
                        SecureSerializer.deserialize(
                            v, allow_restricted, allow_high_risk)
                        for k, v in obj.items()}
        else:
            return obj
