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
        result = {}
        # collect properties defined on class (including inheritance)
        props = {}
        for cls in type(self).mro():
            for name, obj in cls.__dict__.items():
                if isinstance(obj, property) and not name.startswith('_'):
                    props[name] = obj
        for name, prop in props.items():
            try:
                val = getattr(self, name)
            except Exception:
                continue
            result[name] = val
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
        if config is None:
            return cls()
        if not isinstance(config, dict):
            raise ValueError("config must be a dict")
        # map of property name -> property object (with available setter)
        prop_map = {}
        for c in cls.mro():
            for name, obj in c.__dict__.items():
                if isinstance(obj, property) and obj.fset is not None and not name.startswith('_'):
                    prop_map[name] = obj
        obj = cls()
        for key, value in config.items():
            if key not in prop_map:
                raise ValueError(f"Invalid configuration parameter: {key}")
            try:
                setattr(obj, key, value)
            except ValueError as e:
                raise ValueError(f"Invalid value for '{key}': {e}") from e
            except Exception as e:
                raise ValueError(f"Failed setting '{key}': {e}") from e
        return obj
