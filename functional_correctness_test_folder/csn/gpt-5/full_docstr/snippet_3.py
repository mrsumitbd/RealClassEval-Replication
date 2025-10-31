class Serializable:
    '''This is the superclass of all serializable objects.'''

    def save(self, out_file):
        '''Save the model to the given file stream.'''
        # Base class has nothing to save.
        return None

    @classmethod
    def load(cls, in_file, instantiate=True):
        '''This is meant to be overridden by subclasses and called with super.
        We return constructor argument values when not being instantiated. Since there are no
        constructor arguments for the Serializable class we just return an empty dictionary.
        '''
        if not instantiate:
            return {}
        kwargs = cls._instantiated_load(in_file)
        if kwargs is None:
            kwargs = {}
        return cls(**kwargs)

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        '''This is meant to be overridden by subclasses and called with super.
        We return constructor argument values (we have no values to load in this abstract class).
        '''
        return {}
