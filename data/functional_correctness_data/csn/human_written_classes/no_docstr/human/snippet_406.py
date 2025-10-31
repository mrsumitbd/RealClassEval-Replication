class ObjectView:

    def __init__(self, dictionary):
        self.__dict__ = dictionary

    def update(self, obj):
        self.__dict__.update(obj.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        return str(self.__dict__)