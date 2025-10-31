import importlib
import types
import base64
import inspect


class SecureSerializer:
    '''Security-focused serialization system with capability controls for Flock objects.'''

    _TRUSTED_PREFIXES = (
        'builtins',
        'collections',
        'datetime',
        'decimal',
        'fractions',
        'math',
        'operator',
        'functools',
        'itertools',
        'pathlib',
        'types',
        'uuid',
        'typing',
    )
    _RESTRICTED_PREFIXES = (
        'json',
        're',
        'random',
        'statistics',
        'hashlib',
        'hmac',
    )
    _HIGH_RISK_PREFIXES = (
        'os',
        'sys',
        'subprocess',
        'socket',
        'ssl',
        'shutil',
        'tempfile',
        'ctypes',
        'multiprocessing',
        'threading',
        'asyncio',
        'signal',
        'select',
        'resource',
    )

    @staticmethod
    def _get_module_capability(module_name):
        '''Get the capability level for a module.'''
        if not module_name:
            return 'restricted'
        for p in SecureSerializer._TRUSTED_PREFIXES:
            if module_name == p or module_name.startswith(p + '.'):
                return 'trusted'
        for p in SecureSerializer._HIGH_RISK_PREFIXES:
            if module_name == p or module_name.startswith(p + '.'):
                return 'high_risk'
        for p in SecureSerializer._RESTRICTED_PREFIXES:
            if module_name == p or module_name.startswith(p + '.'):
                return 'restricted'
        # Default to restricted if unknown
        return 'restricted'

    @staticmethod
    def _is_safe_callable(obj):
        '''Check if a callable is safe to serialize.'''
        # Allow only top-level functions from trusted modules
        if isinstance(obj, (types.FunctionType, types.BuiltinFunctionType)):
            mod = getattr(obj, '__module__', None)
            if SecureSerializer._get_module_capability(mod) != 'trusted':
                return False
            # Must be top-level, not nested or local
            qn = getattr(obj, '__qualname__', '')
            if '<locals>' in qn:
                return False
            # Must be importable by name
            name = getattr(obj, '__name__', None)
            if not name:
                return False
            try:
                m = importlib.import_module(mod)
                return getattr(m, name, None) is obj
            except Exception:
                return False
        return False

    @staticmethod
    def serialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Serialize an object with capability checks.'''

        def module_allowed(module_name):
            level = SecureSerializer._get_module_capability(module_name)
            if level == 'trusted':
                return True
            if level == 'restricted':
                return allow_restricted
            if level == 'high_risk':
                return allow_high_risk
            return False

        def encode(o):
            # Primitives
            if o is None or isinstance(o, (bool, int, float, str)):
                return o
            # Bytes
            if isinstance(o, (bytes, bytearray, memoryview)):
                data = bytes(o)
                return {
                    '__type__': 'bytes',
                    'data': base64.b64encode(data).decode('ascii'),
                }
            # Lists
            if isinstance(o, list):
                return ['__list__'] + [encode(x) for x in o]
            # Tuples
            if isinstance(o, tuple):
                return {'__type__': 'tuple', 'items': [encode(x) for x in o]}
            # Sets
            if isinstance(o, set):
                return {'__type__': 'set', 'items': [encode(x) for x in o]}
            # Dicts
            if isinstance(o, dict):
                if all(isinstance(k, str) for k in o.keys()):
                    return {k: encode(v) for k, v in o.items()}
                else:
                    return {
                        '__type__': 'dict_items',
                        'items': [[encode(k), encode(v)] for k, v in o.items()],
                    }
            # Callables
            if callable(o):
                if not SecureSerializer._is_safe_callable(o):
                    raise PermissionError('Callable is not safe to serialize')
                mod = getattr(o, '__module__', None)
                name = getattr(o, '__name__', None)
                return {'__type__': 'callable', 'module': mod, 'name': name}
            # Objects
            cls = o.__class__
            mod = getattr(cls, '__module__', None)
            if not module_allowed(mod):
                level = SecureSerializer._get_module_capability(mod)
                raise PermissionError(
                    f'Module capability not allowed: {mod} ({level})')
            # Obtain state
            if hasattr(o, '__getstate__'):
                state = o.__getstate__()
            elif hasattr(o, '__dict__'):
                state = dict(o.__dict__)
            else:
                # As last resort, try dataclass asdict or repr fallback
                try:
                    import dataclasses  # noqa
                    if dataclasses.is_dataclass(o):
                        from dataclasses import asdict
                        state = asdict(o)
                    else:
                        raise AttributeError
                except Exception as e:
                    raise TypeError(
                        f'Cannot serialize object of type {cls.__module__}.{cls.__name__}') from e
            return {
                '__type__': 'object',
                'module': mod,
                'class': cls.__name__,
                'state': encode(state),
            }

        return encode(obj)

    @staticmethod
    def deserialize(obj, allow_restricted=True, allow_high_risk=False):
        '''Deserialize an object with capability enforcement.'''

        def module_allowed(module_name):
            level = SecureSerializer._get_module_capability(module_name)
            if level == 'trusted':
                return True
            if level == 'restricted':
                return allow_restricted
            if level == 'high_risk':
                return allow_high_risk
            return False

        def import_from(module_name, name):
            if not module_allowed(module_name):
                level = SecureSerializer._get_module_capability(module_name)
                raise PermissionError(
                    f'Module capability not allowed: {module_name} ({level})')
            m = importlib.import_module(module_name)
            if not hasattr(m, name):
                raise AttributeError(f'{module_name}.{name} not found')
            return getattr(m, name)

        def decode(o):
            if isinstance(o, (type(None), bool, int, float, str)):
                return o
            if isinstance(o, list):
                if o and len(o) >= 1 and o[0] == '__list__':
                    return [decode(x) for x in o[1:]]
                else:
                    return [decode(x) for x in o]
            if isinstance(o, dict):
                t = o.get('__type__')
                if t == 'bytes':
                    return base64.b64decode(o['data'].encode('ascii'))
                if t == 'tuple':
                    return tuple(decode(x) for x in o['items'])
                if t == 'set':
                    return set(decode(x) for x in o['items'])
                if t == 'dict_items':
                    return {decode(k): decode(v) for k, v in o['items']}
                if t == 'callable':
                    func = import_from(o['module'], o['name'])
                    if not SecureSerializer._is_safe_callable(func):
                        raise PermissionError(
                            'Deserialized callable is not allowed')
                    return func
                if t == 'object':
                    module_name = o['module']
                    class_name = o['class']
                    cls = import_from(module_name, class_name)
                    state = decode(o['state'])
                    # Recreate instance
                    inst = cls.__new__(cls)
                    if hasattr(inst, '__setstate__'):
                        inst.__setstate__(state)
                    elif isinstance(state, dict) and hasattr(inst, '__dict__'):
                        inst.__dict__.update(state)
                    else:
                        # Try dataclass init if possible
                        try:
                            import dataclasses  # noqa
                            if dataclasses.is_dataclass(cls) and isinstance(state, dict):
                                inst = cls(**state)
                            else:
                                raise TypeError
                        except Exception as e:
                            raise TypeError(
                                f'Cannot restore state for {module_name}.{class_name}') from e
                    return inst
                # Regular dict (no type tag)
                return {k: decode(v) for k, v in o.items()}
            # Fallback
            raise TypeError('Unsupported serialized format')

        return decode(obj)
