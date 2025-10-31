
import pickle


class Serializable:

    def save(self, out_file):
        pickle.dump(self, out_file)

    @classmethod
    def load(cls, in_file, instantiate=True):
        if instantiate:
            return cls._instantiated_load(in_file)
        else:
            return pickle.load(in_file)

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        obj = pickle.load(in_file)
        if not isinstance(obj, cls):
            raise ValueError(
                "Loaded object is not an instance of the expected class")
        return obj
