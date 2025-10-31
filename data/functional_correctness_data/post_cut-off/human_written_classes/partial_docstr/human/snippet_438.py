import pickle
import hashlib
from requests import Session as RequestsSession

class RequestsAPIWrapper:
    """Provides a `requests.api`-like interface with a specific validator"""
    SUPPORT_WRAPPER_PICKLING = False

    def __init__(self, validator):
        try:
            from .futures import FuturesSession
            have_requests_futures = True
        except ImportError as e:
            have_requests_futures = False
        self.validator = validator
        outer_self = self

        class _WrappedSession(Session):
            """An `advocate.Session` that uses the wrapper's blacklist

            the wrapper is meant to be a transparent replacement for `requests`,
            so people should be able to subclass `wrapper.Session` and still
            get the desired validation behaviour
            """
            DEFAULT_VALIDATOR = outer_self.validator
        self._make_wrapper_cls_global(_WrappedSession)
        if have_requests_futures:

            class _WrappedFuturesSession(FuturesSession):
                """Like _WrappedSession, but for `FuturesSession`s"""
                DEFAULT_VALIDATOR = outer_self.validator
            self._make_wrapper_cls_global(_WrappedFuturesSession)
            self.FuturesSession = _WrappedFuturesSession
        self.request = self._default_arg_wrapper(request)
        self.get = self._default_arg_wrapper(get)
        self.Session = _WrappedSession

    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            from . import cw_advocate
            return getattr(cw_advocate, item)

    def _default_arg_wrapper(self, fun):

        def wrapped_func(*args, **kwargs):
            kwargs.setdefault('validator', self.validator)
            return fun(*args, **kwargs)
        return wrapped_func

    def _make_wrapper_cls_global(self, cls):
        if not self.SUPPORT_WRAPPER_PICKLING:
            return
        wrapper_hash = hashlib.sha256(pickle.dumps(self)).hexdigest()
        cls.__name__ = '_'.join((cls.__name__, wrapper_hash))
        cls.__qualname__ = '.'.join((__name__, cls.__name__))
        if not globals().get(cls.__name__):
            globals()[cls.__name__] = cls