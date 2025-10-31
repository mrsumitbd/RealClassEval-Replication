
import pickle
import importlib
import types


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''
    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        module_capabilities = {
            'safe_module': 'safe',
            'restricted_module': 'restricted',
            'high_risk_module': 'high_risk'
        }
        return module_capabilities.get(module_name, 'unknown')

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if a callable is safe to serialize.'''
        if not callable(obj):
            return False
        module_name = obj.__module__
        capability = SecureSerializer._get_module_capability(module_name)
        if capability == 'safe':
            return True
        elif capability == 'restricted':
            return SecureSerializer._is_restricted_allowed()
        elif capability == 'high_risk':
            return SecureSerializer._is_high_risk_allowed()
        return False

    @staticmethod
    def _is_restricted_allowed():
        '''Check if restricted modules are allowed.'''
        return True  # This should be controlled by a configuration or parameter

    @staticmethod
    def _is_high_risk_allowed():
        '''Check if high risk modules are allowed.'''
        return False  # This should be controlled by a configuration or parameter

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        if isinstance(obj, types.FunctionType) and not SecureSerializer._is_safe_callable(obj):
            raise ValueError("Object is not safe to serialize.")
        SecureSerializer._is_restricted_allowed = lambda: allow_restricted
        SecureSerializer._is_high_risk_allowed = lambda: allow_high_risk
        return pickle.dumps(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        SecureSerializer._is_restricted_allowed = lambda: allow_restricted
        SecureSerializer._is_high_risk_allowed = lambda: allow_high_risk
        deserialized_obj = pickle.loads(obj)
        if isinstance(deserialized_obj, types.FunctionType) and not SecureSerializer._is_safe_callable(deserialized_obj):
            raise ValueError("Deserialized object is not safe.")
        return deserialized_obj
