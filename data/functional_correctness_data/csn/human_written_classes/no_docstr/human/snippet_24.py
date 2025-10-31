from time import monotonic as current_time
from typing import TYPE_CHECKING, Optional
from sanic.request import Request
from sanic.http.constants import HTTP

class HttpProtocolMixin:
    __slots__ = ()
    __version__: HTTP

    def _setup_connection(self, *args, **kwargs):
        self._http = self.HTTP_CLASS(self, *args, **kwargs)
        self._time = current_time()
        try:
            self.check_timeouts()
        except AttributeError:
            ...

    def _setup(self):
        self.request: Optional[Request] = None
        self.access_log = self.app.config.ACCESS_LOG
        self.request_handler = self.app.handle_request
        self.error_handler = self.app.error_handler
        self.request_timeout = self.app.config.REQUEST_TIMEOUT
        self.response_timeout = self.app.config.RESPONSE_TIMEOUT
        self.keep_alive_timeout = self.app.config.KEEP_ALIVE_TIMEOUT
        self.request_max_size = self.app.config.REQUEST_MAX_SIZE
        self.request_class = self.app.request_class or Request

    @property
    def http(self):
        if not hasattr(self, '_http'):
            return None
        return self._http

    @property
    def version(self):
        return self.__class__.__version__