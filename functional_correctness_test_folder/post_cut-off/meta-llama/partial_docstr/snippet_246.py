
import dill
import inspect


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        # Define a dictionary to map module names to their respective capability levels
        capability_levels = {
            'builtins': 'high_risk',
            'os': 'high_risk',
            'sys': 'high_risk',
            'subprocess': 'high_risk',
            'shutil': 'high_risk',
            'pickle': 'high_risk',
            'dill': 'high_risk',
            '__main__': 'restricted',
        }
        return capability_levels.get(module_name, 'low_risk')

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if an object is a safe callable.'''
        if not inspect.isfunction(obj) and not inspect.ismethod(obj):
            return True  # Not a callable, so it's safe

        module_name = inspect.getmodule(obj).__name__
        capability = SecureSerializer._get_module_capability(module_name)

        if capability == 'high_risk':
            return False
        elif capability == 'restricted':
            # Check if the function is a built-in or has a restricted name
            if obj.__name__.startswith('__') and obj.__name__.endswith('__'):
                return False
        return True

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        try:
            serialized_obj = dill.dumps(obj)
            deserialized_obj = dill.loads(serialized_obj)

            if inspect.isfunction(deserialized_obj) or inspect.ismethod(deserialized_obj):
                module_name = inspect.getmodule(deserialized_obj).__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)

                if capability == 'high_risk' and not allow_high_risk:
                    raise Exception(
                        f"Serialization of high-risk object {obj.__name__} from module {module_name} is not allowed.")
                elif capability == 'restricted' and not allow_restricted:
                    raise Exception(
                        f"Serialization of restricted object {obj.__name__} from module {module_name} is not allowed.")

                if not SecureSerializer._is_safe_callable(deserialized_obj):
                    raise Exception(
                        f"Serialization of unsafe callable {obj.__name__} is not allowed.")

            return serialized_obj
        except Exception as e:
            raise Exception(f"Failed to serialize object: {str(e)}")

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        try:
            deserialized_obj = dill.loads(obj)

            if inspect.isfunction(deserialized_obj) or inspect.ismethod(deserialized_obj):
                module_name = inspect.getmodule(deserialized_obj).__name__
                capability = SecureSerializer._get_module_capability(
                    module_name)

                if capability == 'high_risk' and not allow_high_risk:
                    raise Exception(
                        f"Deserialization of high-risk object {deserialized_obj.__name__} from module {module_name} is not allowed.")
                elif capability == 'restricted' and not allow_restricted:
                    raise Exception(
                        f"Deserialization of restricted object {deserialized_obj.__name__} from module {module_name} is not allowed.")

                if not SecureSerializer._is_safe_callable(deserialized_obj):
                    raise Exception(
                        f"Deserialization of unsafe callable {deserialized_obj.__name__} is not allowed.")

            return deserialized_obj
        except Exception as e:
            raise Exception(f"Failed to deserialize object: {str(e)}")
