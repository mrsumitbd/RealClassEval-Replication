class Factory:
    cache = {}

    @classmethod
    def subclass(cls, name, bases, dict={}):
        if not isinstance(bases, tuple):
            bases = (bases,)
        key = '.'.join((name, str(bases)))
        subclass = cls.cache.get(key)
        if subclass is None:
            subclass = type(name, bases, dict)
            cls.cache[key] = subclass
        return subclass

    @classmethod
    def object(cls, classname=None, dict={}):
        if classname is not None:
            subclass = cls.subclass(classname, Object)
            inst = subclass()
        else:
            inst = Object()
        for a in dict.items():
            setattr(inst, a[0], a[1])
        return inst

    @classmethod
    def metadata(cls):
        return Metadata()

    @classmethod
    def property(cls, name, value=None):
        subclass = cls.subclass(name, Property)
        return subclass(value)