class Factory:
    """
    Factory decorator could be used to define result of a function as default value. It could
    be useful to define a :class:`~dirty_models.fields.DateTimeField` with :meth:`datetime.datetime.now`
    in order to set the current datetime.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()