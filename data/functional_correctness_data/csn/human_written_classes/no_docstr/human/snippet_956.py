class ProceedKeyword:
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton == None:
            cls.__singleton = super(ProceedKeyword, cls).__new__(cls)
        return cls.__singleton

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self