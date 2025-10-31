
import pickle


class Serializable:
    '''This is the superclass of all serializable objects.'''

    def save(self, out_file):
        with open(out_file, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, in_file, instantiate=True):
        with open(in_file, 'rb') as f:
            obj = pickle.load(f)
        if instantiate:
            return obj
        else:
            return obj.__dict__

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        with open(in_file, 'rb') as f:
            obj = pickle.load(f)
        for key, value in kwargs.items():
            setattr(obj, key, value)
        return obj
