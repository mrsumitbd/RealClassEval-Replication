class ConfigParam:

    def __init__(self, default, filter=None, allow_override=True):
        """If allow_override is False, we can't change the value after the
        import of Theano.

        So the value should be the same during all the execution.
        """
        self.default = default
        self.filter = filter
        self.allow_override = allow_override
        self.is_default = True

    def __get__(self, cls, type_, delete_key=False):
        if cls is None:
            return self
        if not hasattr(self, 'val'):
            try:
                val_str = fetch_val_for_key(self.fullname, delete_key=delete_key)
                self.is_default = False
            except KeyError:
                if callable(self.default):
                    val_str = self.default()
                else:
                    val_str = self.default
            self.__set__(cls, val_str)
        return self.val

    def __set__(self, cls, val):
        if not self.allow_override and hasattr(self, 'val'):
            raise Exception("Can't change the value of this config parameter after initialization!")
        if self.filter:
            self.val = self.filter(val)
        else:
            self.val = val