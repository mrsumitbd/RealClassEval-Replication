import inspect
import pickle

class Serializable:
    """This is the superclass of all serializable objects."""

    def save(self, out_file):
        """Save the model to the given file stream."""
        pickle.dump(type(self), out_file)

    @classmethod
    def load(cls, in_file, instantiate=True):
        """This is meant to be overridden by subclasses and called with super.

        We return constructor argument values when not being instantiated. Since there are no
        constructor arguments for the Serializable class we just return an empty dictionary.
        """
        if instantiate:
            return cls._instantiated_load(in_file)
        return {}

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        """This is meant to be overridden by subclasses and called with super.

        We return constructor argument values (we have no values to load in this abstract class).
        """
        obj_type = pickle.load(in_file)
        if obj_type is None:
            return None
        if not inspect.isclass(obj_type) or (not issubclass(obj_type, cls) and obj_type is not cls):
            raise Exception(f'Invalid object type loaded from file. {obj_type} is not a subclass of {cls}.')
        constructor_args = obj_type.load(in_file, instantiate=False, **kwargs)
        used_args = inspect.getfullargspec(obj_type.__init__)[0]
        return obj_type(**{k: constructor_args[k] for k in constructor_args if k in used_args})