
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
        for name in dir(self):
            # Skip private attributes and methods
            if name.startswith('_'):
                continue
            attr = getattr(self.__class__, name, None)
            if isinstance(attr, property):
                try:
                    value = getattr(self, name)
                except Exception:
                    # If the getter raises, skip this property
                    continue
                result[name] = value
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
            raise ValueError('config must be a dictionary')

        instance = cls()
        for key, value in config.items():
            # Validate that the key corresponds to a property
            prop = getattr(cls, key, None)
            if not isinstance(prop, property):
                raise ValueError(f'Unknown configuration parameter: {key}')
            try:
                setattr(instance, key, value)
            except Exception as e:
                raise ValueError(f'Invalid value for {key}: {e}') from e
        return instance
