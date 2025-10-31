class _TaskConfig:

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k.isidentifier()}

    @classmethod
    def from_dict(cls, config):
        if config is None:
            return cls()
        if not isinstance(config, dict):
            raise TypeError("config must be a dict")
        inst = cls()
        for k, v in config.items():
            if isinstance(k, str) and k.isidentifier():
                setattr(inst, k, v)
        return inst
