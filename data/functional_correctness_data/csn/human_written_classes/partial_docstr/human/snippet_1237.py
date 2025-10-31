import functools

class validates:
    """A decorator to store validators.

    :param args: Validator objects
    """

    def __init__(self, *args):
        self.validators = list(args)

    def __call__(self, func):
        for validator in self.validators:
            validator.func_name = func.__name__

        @functools.wraps(func)
        def wrapper(instance, value):
            for validator in self.validators:
                validator(value)
            return func(instance, value)
        return wrapper