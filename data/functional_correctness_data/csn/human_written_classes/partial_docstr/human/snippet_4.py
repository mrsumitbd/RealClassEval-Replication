from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import InvalidArgumentException

class _ProxyDescriptor:
    """:Returns: Proxy if set, otherwise None."""

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls):
        return obj._proxy

    def __set__(self, obj, value):
        if not isinstance(value, Proxy):
            raise InvalidArgumentException('Only Proxy objects can be passed in.')
        obj._proxy = value
        obj._caps[self.name] = value.to_capabilities()