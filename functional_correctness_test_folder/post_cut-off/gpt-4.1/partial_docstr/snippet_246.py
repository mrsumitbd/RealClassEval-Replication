
import pickle
import types
import builtins


class SecureSerializer:

    # Capability levels:
    # 0: safe (builtins, math, etc.)
    # 1: restricted (os, sys, etc.)
    # 2: high risk (subprocess, socket, etc.)
    _module_capabilities = {
        'builtins': 0,
        'math': 0,
        'datetime': 0,
        'collections': 0,
        'os': 1,
        'sys': 1,
        'shutil': 1,
        'subprocess': 2,
        'socket': 2,
        'multiprocessing': 2,
        'threading': 1,
        'ctypes': 2,
        'pickle': 1,
        'importlib': 1,
        'platform': 1,
        'signal': 1,
        'resource': 2,
        'ssl': 2,
        'http': 2,
        'urllib': 2,
        'xml': 1,
        'json': 0,
        're': 0,
        'random': 0,
        'hashlib': 0,
        'logging': 1,
        'email': 1,
        'csv': 0,
        'copy': 0,
        'functools': 0,
        'itertools': 0,
        'operator': 0,
        'types': 0,
        'enum': 0,
        'pathlib': 0,
        'time': 0,
        'inspect': 1,
        'warnings': 1,
        'traceback': 1,
        'pprint': 0,
        'array': 0,
        'heapq': 0,
        'bisect': 0,
        'weakref': 0,
        'uuid': 0,
        'typing': 0,
        'dataclasses': 0,
        'abc': 0,
        'queue': 1,
        'concurrent': 1,
        'asyncio': 1,
        'selectors': 1,
        'select': 1,
        'socketserver': 2,
        'xmlrpc': 2,
        'bz2': 1,
        'lzma': 1,
        'zipfile': 1,
        'tarfile': 1,
        'glob': 0,
        'fnmatch': 0,
        'tempfile': 1,
        'getpass': 1,
        'pwd': 1,
        'grp': 1,
        'spwd': 1,
        'crypt': 1,
        'termios': 1,
        'tty': 1,
        'pty': 1,
        'fcntl': 1,
        'resource': 2,
        'syslog': 1,
        'signal': 1,
        'faulthandler': 1,
        'trace': 1,
        'tracemalloc': 1,
        'cProfile': 1,
        'profile': 1,
        'pstats': 1,
        'marshal': 2,
        'codecs': 1,
        'encodings': 1,
        'bz2': 1,
        'lzma': 1,
        'zipfile': 1,
        'tarfile': 1,
        'zlib': 1,
        'gzip': 1,
        'bz2': 1,
        'lzma': 1,
        'zipfile': 1,
        'tarfile': 1,
        'zlib': 1,
        'gzip': 1,
        'bz2': 1,
        'lzma': 1,
        'zipfile': 1,
        'tarfile': 1,
        'zlib': 1,
        'gzip': 1,
    }

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        return SecureSerializer._module_capabilities.get(module_name, 1)

    @staticmethod
    def _is_safe_callable(obj):
        # Only allow built-in functions, methods, and functions from safe modules
        if isinstance(obj, (types.BuiltinFunctionType, types.BuiltinMethodType)):
            return True
        if isinstance(obj, types.FunctionType):
            mod = getattr(obj, '__module__', None)
            if mod is None:
                return False
            return SecureSerializer._get_module_capability(mod) == 0
        if isinstance(obj, types.MethodType):
            func = obj.__func__
            mod = getattr(func, '__module__', None)
            if mod is None:
                return False
            return SecureSerializer._get_module_capability(mod) == 0
        return False

    @staticmethod
    def _check_obj_capability(obj, allow_restricted, allow_high_risk):
        # Recursively check the object's module and any callables
        # For classes and functions, check their module
        if isinstance(obj, (types.FunctionType, types.BuiltinFunctionType, types.MethodType)):
            mod = getattr(obj, '__module__', None)
            cap = SecureSerializer._get_module_capability(mod)
            if cap == 2 and not allow_high_risk:
                raise ValueError(f"High risk module '{mod}' not allowed")
            if cap == 1 and not allow_restricted:
                raise ValueError(f"Restricted module '{mod}' not allowed")
        elif isinstance(obj, type):
            mod = getattr(obj, '__module__', None)
            cap = SecureSerializer._get_module_capability(mod)
            if cap == 2 and not allow_high_risk:
                raise ValueError(f"High risk module '{mod}' not allowed")
            if cap == 1 and not allow_restricted:
                raise ValueError(f"Restricted module '{mod}' not allowed")
        elif isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                SecureSerializer._check_obj_capability(
                    item, allow_restricted, allow_high_risk)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                SecureSerializer._check_obj_capability(
                    k, allow_restricted, allow_high_risk)
                SecureSerializer._check_obj_capability(
                    v, allow_restricted, allow_high_risk)
        elif hasattr(obj, '__dict__'):
            for v in vars(obj).values():
                SecureSerializer._check_obj_capability(
                    v, allow_restricted, allow_high_risk)
        # else: assume safe (int, str, float, etc.)

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''
        SecureSerializer._check_obj_capability(
            obj, allow_restricted, allow_high_risk)
        return pickle.dumps(obj, protocol=4)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''
        loaded = pickle.loads(obj)
        SecureSerializer._check_obj_capability(
            loaded, allow_restricted, allow_high_risk)
        return loaded
