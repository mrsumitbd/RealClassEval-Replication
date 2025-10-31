
import pickle


class Serializable:

    def save(self, out_file):
        """Saves the object to a file using pickle."""
        with open(out_file, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, in_file, instantiate=True):
        """Loads an object from a file using pickle."""
        with open(in_file, 'rb') as f:
            if instantiate:
                return pickle.load(f)
            else:
                return f

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        """Loads an object from a file and checks if it's an instance of the class."""
        obj = cls.load(in_file)
        if not isinstance(obj, cls):
            raise TypeError(
                f"Loaded object is not an instance of {cls.__name__}")
        return obj
