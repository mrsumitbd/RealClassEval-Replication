class ExceptionWrapper:
    """
    Create a dummy object which will raise an exception when attributes
    are accessed (i.e. when used as a module) or when called (i.e.
    when used like a function)

    For soft dependencies we want to survive failing to import but
    we would like to raise an appropriate error when the functionality is
    actually requested so the user gets an easily debuggable message.
    """

    def __init__(self, exception: BaseException):
        self.exception = (type(exception), exception.args)

    def __getattribute__(self, *args, **kwargs):
        if args[0] == '__class__':
            return None.__class__
        exc_type, exc_args = super().__getattribute__('exception')
        raise exc_type(*exc_args)

    def __call__(self, *args, **kwargs):
        self.__getattribute__('exception')