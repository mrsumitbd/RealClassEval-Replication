
import pickle
import inspect
import types


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''
    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        if module_name in ['pickle', 'marshal', 'shelve', 'dbm']:
            return 'high_risk'
        elif module_name in ['json', 'yaml']:
            return 'restricted'
        else:
            return 'safe'

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if a callable is safe to serialize.'''
        if not callable(obj):
            return False
        module = inspect.getmodule(obj)
        if module is None:
            return False
        module_name = module.__name__
        capability = SecureSerializer._get_module_capability(module_name)
        if capability == 'high_risk':
            return False
        elif capability == 'restricted':
            return False
        return True

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        if not allow_restricted and isinstance(obj, (types.FunctionType, types.MethodType)):
            module = inspect.getmodule(obj)
            if module is not None:
                module_name = module.__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'restricted':
                    raise ValueError(
                        "Serialization of restricted callables is not allowed.")
        if not allow_high_risk and isinstance(obj, (types.FunctionType, types.MethodType)):
            module = inspect.getmodule(obj)
            if module is not None:
                module_name = module.__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'high_risk':
                    raise ValueError(
                        "Serialization of high-risk callables is not allowed.")
        return pickle.dumps(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        deserialized_obj = pickle.loads(obj)
        if not allow_restricted and isinstance(deserialized_obj, (types.FunctionType, types.MethodType)):
            module = inspect.getmodule(deserialized_obj)
            if module is not None:
                module_name = module.__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'restricted':
                    raise ValueError(
                        "Deserialization of restricted callables is not allowed.")
        if not allow_high_risk and isinstance(deserialized_obj, (types.FunctionType, types.MethodType)):
            module = inspect.getmodule(deserialized_obj)
            if module is not None:
                module_name = module.__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)
                if capability == 'high_risk':
                    raise ValueError(
                        "Deserialization of high-risk callables is not allowed.")
        return deserialized_obj
