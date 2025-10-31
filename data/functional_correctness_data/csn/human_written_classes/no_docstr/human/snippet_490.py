class NotSet:
    __slots__ = ()

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __repr__(self):
        return 'NOT_SET'