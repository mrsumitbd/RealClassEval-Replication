
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

    def __init__(self, schedule, archive):
        self.schedule = schedule
        self.archive = archive

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, value):
        if not isinstance(value, str):
            raise ValueError("Schedule must be a string.")
        self._schedule = value

    @property
    def archive(self):
        return self._archive

    @archive.setter
    def archive(self, value):
        if not isinstance(value, bool):
            raise ValueError("Archive must be a boolean.")
        self._archive = value

    def to_dict(self):
        '''Returns a dict with the representation of this task configuration object.'''
        return {
            'schedule': self.schedule,
            'archive': self.archive
        }

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
        return cls(
            schedule=config.get('schedule'),
            archive=config.get('archive')
        )
