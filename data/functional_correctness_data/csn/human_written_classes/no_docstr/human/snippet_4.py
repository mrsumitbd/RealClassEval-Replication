import warnings

class _ProxyTypeDescriptor:

    def __init__(self, name, p_type):
        self.name = name
        self.p_type = p_type

    def __get__(self, obj, cls):
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if self.name == 'autodetect' and (not isinstance(value, bool)):
            raise ValueError('Autodetect proxy value needs to be a boolean')
        if self.name == 'ftpProxy':
            warnings.warn('ftpProxy is deprecated and will be removed in the future', DeprecationWarning, stacklevel=2)
        getattr(obj, '_verify_proxy_type_compatibility')(self.p_type)
        setattr(obj, 'proxyType', self.p_type)
        setattr(obj, self.name, value)