
class Serializable:
    '''This is the superclass of all serializable objects.'''

    def save(self, out_file):
        '''Save the model to the given file stream.'''
        # For the base class, nothing to save.
        pass

    @classmethod
    def load(cls, in_file, instantiate=True):
        '''This is meant to be overridden by subclasses and called with super.
        We return constructor argument values when not being instantiated. Since there are no
        constructor arguments for the Serializable class we just return an empty dictionary.
        '''
        if instantiate:
            return cls._instantiated_load(in_file)
        else:
            # No constructor arguments for Serializable
            return {}

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        '''This is meant to be overridden by subclasses and called with super.
        We return constructor argument values (we have no values to load in this abstract class).
        '''
        # No arguments to pass to constructor
        return cls()
