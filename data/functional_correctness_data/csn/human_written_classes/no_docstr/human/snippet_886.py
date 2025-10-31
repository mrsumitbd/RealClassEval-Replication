import warnings
import contextlib

class CachedAttribute:

    def __init__(self, func, cachename=None, resetlist=None):
        self.fget = func
        self.name = func.__name__
        self.cachename = cachename or '_cache'
        self.resetlist = resetlist or ()

    def __get__(self, obj, type_=None):
        if obj is None:
            return self.fget
        _cachename = self.cachename
        _cache = getattr(obj, _cachename, None)
        if _cache is None:
            setattr(obj, _cachename, resettable_cache())
            _cache = getattr(obj, _cachename)
        name = self.name
        _cachedval = _cache.get(name, None)
        if _cachedval is None:
            _cachedval = self.fget(obj)
            try:
                _cache[name] = _cachedval
            except KeyError:
                setattr(_cache, name, _cachedval)
            resetlist = self.resetlist
            if resetlist != ():
                with contextlib.suppress(AttributeError):
                    _cache._resetdict[name] = self.resetlist
        return _cachedval

    def __set__(self, obj, value):
        errmsg = f"The attribute '{self.name}' cannot be overwritten"
        warnings.warn(errmsg, CacheWriteWarning, stacklevel=2)