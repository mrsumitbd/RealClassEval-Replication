
import json
import os


class Serializable:

    def save(self, out_file):
        with open(out_file, 'w') as f:
            json.dump(self.__dict__, f)

    @classmethod
    def load(cls, in_file, instantiate=True):
        with open(in_file, 'r') as f:
            data = json.load(f)
        if instantiate:
            return cls._instantiated_load(in_file, **data)
        return data

    @classmethod
    def _instantiated_load(cls, in_file, **kwargs):
        instance = cls.__new__(cls)
        instance.__dict__.update(kwargs)
        return instance
