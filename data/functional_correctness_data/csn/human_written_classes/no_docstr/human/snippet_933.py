class _Settings:

    def __init__(self):
        self.__dict__ = {}

    def update(self, new):
        for name in dir(new):
            if name.isupper():
                self.__dict__[name] = getattr(new, name)