
import io
import pickle
import types
import builtins
import importlib


class SecureSerializer:

    @staticmethod
    def _get_module_capability(module_name):
        # Define risk levels for some common modules
        high_risk = {'os', 'sys', 'subprocess', 'socket', 'shutil', 'ctypes'}
        restricted = {'pickle', 'marshal', 'imp', 'importlib', 'builtins'}
        if module_name in high_risk:
            return 'high_risk'
        elif module_name in restricted:
            return 'restricted'
        else:
            return 'safe'

    @staticmethod
    def _is_safe_callable(obj):
        # Only allow built-in functions and user-defined functions, not lambdas or methods
        if isinstance(obj, types.BuiltinFunctionType):
            return True
        if isinstance(obj, types.FunctionType):
            # Disallow lambdas
            if obj.__name__ == "<lambda>":
                return False
            # Disallow functions from high-risk or restricted modules
            mod = obj.__module__
            cap = SecureSerializer._get_module_capability(mod)
            if cap == 'high_risk':
                return False
            return True
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        # Check for high-risk or restricted objects
        def check_obj(o):
            if isinstance(o, types.FunctionType):
                mod = o.__module__
                cap = SecureSerializer._get_module_capability(mod)
                if cap == 'high_risk' and not allow_high_risk:
                    raise ValueError(
                        f"High-risk function from module '{mod}' cannot be serialized.")
                if cap == 'restricted' and not allow_restricted:
                    raise ValueError(
                        f"Restricted function from module '{mod}' cannot be serialized.")
            elif isinstance(o, type):
                mod = o.__module__
                cap = SecureSerializer._get_module_capability(mod)
                if cap == 'high_risk' and not allow_high_risk:
                    raise ValueError(
                        f"High-risk class from module '{mod}' cannot be serialized.")
                if cap == 'restricted' and not allow_restricted:
                    raise ValueError(
                        f"Restricted class from module '{mod}' cannot be serialized.")
            elif isinstance(o, (list, tuple, set)):
                for item in o:
                    check_obj(item)
            elif isinstance(o, dict):
                for k, v in o.items():
                    check_obj(k)
                    check_obj(v)
            # else: ignore other types

        check_obj(obj)
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        # Custom Unpickler to restrict loading of high-risk/restricted modules
        class RestrictedUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                cap = SecureSerializer._get_module_capability(module)
                if cap == 'high_risk' and not allow_high_risk:
                    raise pickle.UnpicklingError(
                        f"High-risk module '{module}' is not allowed.")
                if cap == 'restricted' and not allow_restricted:
                    raise pickle.UnpicklingError(
                        f"Restricted module '{module}' is not allowed.")
                # Only allow builtins and safe modules
                if module == "builtins":
                    return getattr(builtins, name)
                mod = importlib.import_module(module)
                return getattr(mod, name)
        return RestrictedUnpickler(io.BytesIO(obj)).load()
