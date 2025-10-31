class ConfigGroup:

    def __init__(self, section):
        self.__dict__['_section'] = section

    def __dir__(self):
        return list(self.__dict__['_section'].keys())

    def __getattr__(self, k):
        return _val_xform(self.__dict__['_section'][k])
    __getitem__ = __getattr__

    def __setattr__(self, k, v):
        logger.info(str(self.__class__.__name__) + '.__setattr__({k}, ...)'.format(k=k))
        self.__dict__['_section'][k] = str(v)
    __setitem__ = __setattr__