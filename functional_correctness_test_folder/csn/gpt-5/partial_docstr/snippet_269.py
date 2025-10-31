class _TaskConfig:
    '''Abstract class to store task configuration options.
    This class defines how to store specific task configuration
    arguments such as scheduling or archiving options. It is not
    meant to be instantiated on its own.
    Configuration options must be defined using `property` and `setter`
    decorators. Setters must check whether the given value is valid
    or not. When it is invalid, a `ValueError` exception should be
    raised. The rationale behind this is to use these methods as
    parsers when `from_dict` class method is called. It will create
    a new instance of the subclass passing its properties from a
    dictionary.
    '''

    def to_dict(self):
        '''Returns a dict with the representation of this task configuration object.'''
        props = {
            name: prop
            for name, prop in self._iter_properties()
            if prop.fget is not None
        }
        result = {}
        for name in props:
            result[name] = getattr(self, name)
        return result

    @classmethod
    def from_dict(cls, config):
        '''Create an configuration object from a dictionary.
        Key,value pairs will be used to initialize a task configuration
        object. If 'config' contains invalid configuration parameters
        a `ValueError` exception will be raised.
        :param config: dictionary used to create an instance of this object
        :returns: a task config instance
        :raises ValueError: when an invalid configuration parameter is found
        '''
        if not isinstance(config, dict):
            raise ValueError("config must be a dict")

        prop_map = {name: prop for name, prop in cls._iter_properties()}
        valid_settable = {name for name,
                          p in prop_map.items() if p.fset is not None}

        unknown = set(config.keys()) - set(prop_map.keys())
        if unknown:
            raise ValueError(
                f"Unknown configuration parameter(s): {', '.join(sorted(unknown))}")

        unsettable = {k for k in config.keys() if k not in valid_settable}
        if unsettable:
            raise ValueError(
                f"Read-only or unsettable configuration parameter(s): {', '.join(sorted(unsettable))}")

        try:
            obj = cls()
        except TypeError as e:
            raise ValueError(
                f"Could not instantiate {cls.__name__} without arguments") from e

        for key, value in config.items():
            try:
                setattr(obj, key, value)
            except ValueError as ve:
                raise ValueError(
                    f"Invalid value for parameter '{key}': {ve}") from ve
            except Exception as e:
                raise ValueError(
                    f"Failed setting parameter '{key}': {e}") from e

        return obj

    @classmethod
    def _iter_properties(cls):
        # Collect properties defined on the class and its bases, excluding those from object
        props = {}
        for c in cls.mro():
            if c is object:
                continue
            for name, attr in c.__dict__.items():
                if isinstance(attr, property):
                    props[name] = attr
        # Preserve definition order where possible
        for name, prop in props.items():
            yield name, prop
