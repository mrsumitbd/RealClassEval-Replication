
class _TaskConfig:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, config):
        return cls(**config)
