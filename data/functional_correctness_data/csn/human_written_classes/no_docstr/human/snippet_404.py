class _NoneObject:

    def __init__(self, description):
        self.description = description

    def __getattr__(self, item):
        raise AttributeError(f"'{self.__class__.__name__}' for «'{self.description}'» has no attribute '{item}'")

    def __bool__(self):
        return False