
import pickle


class Serializable:

    def save(self, out_file):

        with open(out_file, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, in_file, instantiate=True):

        with open(in_file, 'rb') as f:
            if instantiate:
                return cls._instantiated_load(f)
            else:
                return pickle.load(f)

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):

        obj = pickle.load(in_file)
        if isinstance(obj, cls):
            return obj
        else:
            raise TypeError(
                f"Loaded object is not an instance of {cls.__name__}")
