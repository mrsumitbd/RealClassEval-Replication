
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
        for attr in dir(self.__class__):
            prop = getattr(self.__class__, attr)
            if isinstance(prop, property):
                result[attr] = getattr(self, attr)
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
        # Find all property names
        prop_names = {name for name, val in vars(
            cls).items() if isinstance(val, property)}
        # Check for invalid keys
        for key in config:
            if key not in prop_names:
                raise ValueError(f"Invalid configuration parameter: {key}")
        # Create instance
        obj = cls.__new__(cls)
        # Set properties using setters (which will validate)
        for name in prop_names:
            if name in config:
                setattr(obj, name, config[name])
            else:
                # Try to set to default if possible, else leave as is
                pass
        # Optionally, call __init__ if it does not require arguments
        if hasattr(obj, '__init__'):
            try:
                obj.__init__()
            except TypeError:
                # __init__ requires arguments, skip
                pass
        return obj
