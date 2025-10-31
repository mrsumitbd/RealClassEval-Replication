
class _TaskConfig:

    def to_dict(self):

        return self.__dict__

    @classmethod
    def from_dict(cls, config):

        instance = cls()
        instance.__dict__.update(config)
        return instance
