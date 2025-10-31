class ContextFlag:
    '''A context manager which is also used as a boolean flag value within the default sigint handler.
    Its main use is as a flag to prevent the SIGINT handler in cmd2 from raising a KeyboardInterrupt
    while a critical code section has set the flag to True. Because signal handling is always done on the
    main thread, this class is not thread-safe since there is no need.
        '''

    def __init__(self) -> None:
        '''When this flag has a positive value, it is considered set. When it is 0, it is not set.
        It should never go below 0.
        '''
        self._value = 0

    def __bool__(self) -> bool:
        '''Define the truth value of an object when it is used in a boolean context.'''
        return self._value > 0

    def __enter__(self) -> None:
        '''When a with block is entered, the __enter__ method of the context manager is called.'''
        self._value += 1
        return None

    def __exit__(self, *args: object) -> None:
        '''When the execution flow exits a with statement block this is called, regardless of whether an exception occurred.'''
        if self._value > 0:
            self._value -= 1
        else:
            self._value = 0
        return None
