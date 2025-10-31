import re
from grimoirelab_toolkit.introspect import find_class_properties

class _TaskConfig:
    """Abstract class to store task configuration options.

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
    """
    KW_ARGS_ERROR_REGEX = re.compile("^.+ got an unexpected keyword argument '(.+)'$")

    def to_dict(self):
        """Returns a dict with the representation of this task configuration object."""
        properties = find_class_properties(self.__class__)
        config = {name: self.__getattribute__(name) for name, _ in properties}
        return config

    @classmethod
    def from_dict(cls, config):
        """Create an configuration object from a dictionary.

        Key,value pairs will be used to initialize a task configuration
        object. If 'config' contains invalid configuration parameters
        a `ValueError` exception will be raised.

        :param config: dictionary used to create an instance of this object

        :returns: a task config instance

        :raises ValueError: when an invalid configuration parameter is found
        """
        try:
            obj = cls(**config)
        except TypeError as e:
            m = cls.KW_ARGS_ERROR_REGEX.match(str(e))
            if m:
                raise ValueError("unknown '%s' task config parameter" % m.group(1))
            else:
                raise e
        else:
            return obj