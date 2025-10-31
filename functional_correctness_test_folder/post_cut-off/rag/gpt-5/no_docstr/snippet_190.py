from typing import Any


class ClassWithInitArgs:
    '''
    Wrapper class that stores constructor arguments for deferred instantiation.
    This class is particularly useful for remote class instantiation where
    the actual construction needs to happen at a different time or location.
    '''

    def __init__(self, cls, *args, **kwargs) -> None:
        '''Initialize the ClassWithInitArgs instance.
        Args:
            cls: The class to be instantiated later
            *args: Positional arguments for the class constructor
            **kwargs: Keyword arguments for the class constructor
        '''
        if not callable(cls):
            raise TypeError("cls must be a class or other callable.")
        self.cls = cls
        self.args = tuple(args)
        self.kwargs = dict(kwargs)

    def __call__(self) -> Any:
        '''Instantiate the stored class with the stored arguments.'''
        return self.cls(*self.args, **self.kwargs)
